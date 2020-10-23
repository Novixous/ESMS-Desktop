from core.klist import KMDList
from widgets.checkin_screen.shift_item import ShiftItem
from datetime import datetime
import requests

class Shift():

  def __init__(self, shid=None, shift_start=None, shift_end=None, status_id=None):
    self.shid = shid
    self._shift_start = shift_start
    self._shift_end = shift_end
    self.status_id = status_id

  @property
  def shift_name(self):
    shno = f'0000{self.shid}'
    return f'Shift No.{shno[(len(shno) - 4):]}'

  @property
  def shift_start(self):
    return datetime.strptime(
        self._shift_start,
        '%Y-%m-%dT%H:%M:%S.%fZ'
      ).strftime(
        '%d/%m/%Y at %H:%M:%S'
      ) if self._shift_start is not None else None

  @property
  def shift_end(self):
    return datetime.strptime(
        self._shift_end,
        '%Y-%m-%dT%H:%M:%S.%fZ'
      ).strftime(
        '%d/%m/%Y at %H:%M:%S'
      ) if self._shift_end is not None else None

class ShiftList(KMDList):

  def __init__(self, **kwargs):
    super(ShiftList, self).__init__(**kwargs)

  def load_shift(self):
    if self.app.token is not None:
      bearer_token = f'Bearer {self.app.token}'
      headers = {'Authorization': bearer_token}
      response = requests.get(
        f'{self.app.end_point}/shifts',
        headers=headers
      )
      # print('===========\n====load shift', response, response.json())
      json_respone = response.json()
      shifts = []
      data = json_respone['message']
      for d in data:
        shift = Shift(
          shid=d['id'],
          shift_start=d['shiftStart'],
          shift_end=d['shiftEnd'],
          status_id=d['statusId']
        )
        shifts.append(shift)
      if len(shifts) > 0:
        self.clear_shift()
        self.app.activeshiftlist.clear_shift()
        self.app.activeshiftlist.add_shift(
          ShiftItem(
            shift=shifts.pop(0),
            is_to_checkin=True,
            skip_self_register=True
          )
        )
        for sh in shifts:
          self.add_widget(
            ShiftItem(
              shift=sh,
              skip_self_register=True
            )
          )

  def clear_shift(self):
    self.clear_widgets()
