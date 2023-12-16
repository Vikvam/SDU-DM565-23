from abc import ABC, abstractmethod


class NameResolverBase(ABC):
    @abstractmethod
    def find_name(self, item):
        pass
