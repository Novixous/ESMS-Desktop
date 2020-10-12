from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Subject(ABC):
  """
  The Subject interface declares a set of methods for managing subscribers.
  """

  @abstractmethod
  def attach(self, observer: Observer) -> None:
    """
    Attach an observer to the subject.
    """
    pass

  @abstractmethod
  def detach(self, observer: Observer) -> None:
    """
    Detach an observer from the subject.
    """
    pass

  @abstractmethod
  def notify(self) -> None:
    """
    Notify all observers about an event.
    """
    pass


class ConcreteSubject(Subject):
  """
  The Subject owns some important state and notifies observers when the state
  changes.
  """

  _state: int = 0
  """
  For the sake of simplicity, the Subject's state, essential to all
  subscribers, is stored in this variable.
  """

  _observers: List[Observer] = []
  """
  List of subscribers. In real life, the list of subscribers can be stored
  more comprehensively (categorized by event type, etc.).
  """

  def attach(self, observer: Observer) -> None:
    print("Subject: Attached an observer.")
    self._observers.append(observer)

  def detach(self, observer: Observer) -> None:
    self._observers.remove(observer)

  def detachAll(self) -> None:
    self._observers.clear()

  """
  The subscription management methods.
  """

  def notify(self) -> None:
    """
    Trigger an update in each subscriber.
    """

    print("Subject: Notifying observers...")
    for observer in self._observers:
        observer.update(self)

  def send_termination_signal(self) -> None:
    print("\nSubject: I'm doing something important.")
    self._state = 1

    print(f"Subject: My state has just changed to: {self._state}")
    self.notify()


class Observer(ABC):
  """
  The Observer interface declares the update method, used by subjects.
  """

  @abstractmethod
  def update(self, subject: Subject) -> None:
    """
    Receive update from subject.
    """
    pass


"""
Concrete Observers react to the updates issued by the Subject they had been
attached to.
"""


class ConcreteObserver(Observer):
  callback = None
  def update(self, subject: Subject) -> None:
    if subject._state == 1 and callback is not None:
      callback()



# if __name__ == "__main__":
#     # The client code.

#     subject = ConcreteSubject()

#     observer_a = ConcreteObserverA()
#     subject.attach(observer_a)

#     observer_b = ConcreteObserverB()
#     subject.attach(observer_b)

#     subject.some_business_logic()
#     subject.some_business_logic()

#     subject.detach(observer_a)

#     subject.some_business_logic()
