from dataclasses import dataclass
from abc import ABC, abstractmethod, abstractclassmethod
from itertools import count
from functools import wraps
from inspect import signature

# 'start' --> A|B
#              ∟ 'A (MISSING stick)' --> 'B'
#              ∟ 'B' --> C|D
#                         ∟ 'C (win!)'
#                         ∟ 'D (lose)'

class Contract(ABC):
    
    def __set_name__(self, cls, name):
        # print(f'cls: {cls}, name: {name}')
        self.name = f'_{name}'

    def __get__(self, instance, objtype=None):
        # return getattr(instance, self.private_name)
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.name, value)

    @abstractclassmethod
    def validate(self, value):
        pass

class Typed(Contract):
    type = None
    @classmethod
    def validate(cls, value):
        assert isinstance(value, cls.type), f'Expected {cls.type}'
        super().validate(value)

class Integer(Typed):
    type = int

class Base:
    def __init_subclass__(cls):
        for name, val in cls.__annotations__.items():
            contract = val()
            contract.__set_name__(cls, name)
            setattr(cls, name, contract)

class Dummy(ABC):
    # @abstractmethod
    def scene(self):
        return NotImplemented

    def __init__(self, story=None):
        self.story = story
        self.scene() 

    def method(self):
        pass

class DummyType(Typed):
    type = Dummy
    def validate(cls, value):
        print('v2')

        super().validate(value)

class Page(Base):
    num: Integer
    string: DummyType
    def __init__(self, num, string=Dummy()):
        self.num = num
        self.string = string
    
# class BaseStory(ABC):
    pass
    # @abstractmethod
    # def play(self):
    #     return NotImplemented
    
    # @abstractmethod
    # def get_options(self):
    #     return NotImplemented

@dataclass
class Story1(BaseStory):
    steps: list[Page]

    def __iter__(self):
        self.n = -1
        return self
    
    def __next__(self):
        self.n += 1
        if self.n < len(self.steps):
            return self.steps[self.n]
        else:
            raise StopIteration



if __name__ == '__main__':
    s = Story1(('0','1', '2'))
    p = Page(42)
    breakpoint()
    a=42


# class Target:
#     """
#     The Target defines the domain-specific interface used by the client code.
#     """

#     def request(self) -> str:
#         return "Target: The default target's behavior."


# class Adaptee:
#     """
#     The Adaptee contains some useful behavior, but its interface is incompatible
#     with the existing client code. The Adaptee needs some adaptation before the
#     client code can use it.
#     """

#     def specific_request(self) -> str:
#         return ".eetpadA eht fo roivaheb laicepS"


# class Adapter(Target, Adaptee):
#     """
#     The Adapter makes the Adaptee's interface compatible with the Target's
#     interface via multiple inheritance.
#     """

#     def request(self) -> str:
#         return f"Adapter: (TRANSLATED) {self.specific_request()[::-1]}"


# def client_code(target: "Target") -> None:
#     """
#     The client code supports all classes that follow the Target interface.
#     """

#     print(target.request(), end="")


# if __name__ == "__main__":
#     print("Client: I can work just fine with the Target objects:")
#     target = Target()
#     client_code(target)
#     print("\n")

#     adaptee = Adaptee()
#     print("Client: The Adaptee class has a weird interface. "
#           "See, I don't understand it:")
#     print(f"Adaptee: {adaptee.specific_request()}", end="\n\n")

#     print("Client: But I can work with it via the Adapter:")
#     adapter = Adapter()
#     client_code(adapter)