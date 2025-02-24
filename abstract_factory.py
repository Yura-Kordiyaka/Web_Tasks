from abc import ABC, abstractmethod

class Car(ABC):
    @abstractmethod
    def drive(self):
        pass

class Bike(ABC):
    @abstractmethod
    def ride(self):
        pass

class Sedan(Car):
    def drive(self):
        return "Driving a sedan."

class SUV(Car):
    def drive(self):
        return "Driving an SUV."

class MountainBike(Bike):
    def ride(self):
        return "Riding a mountain bike."

class RoadBike(Bike):
    def ride(self):
        return "Riding a road bike."

class TransportFactory(ABC):
    @abstractmethod
    def create_car(self):
        pass

    @abstractmethod
    def create_bike(self):
        pass

class CityTransportFactory(TransportFactory):
    def create_car(self):
        return Sedan()

    def create_bike(self):
        return RoadBike()

class MountainTransportFactory(TransportFactory):
    def create_car(self):
        return SUV()

    def create_bike(self):
        return MountainBike()

def get_transport(factory: TransportFactory):
    car = factory.create_car()
    bike = factory.create_bike()
    return car.drive(), bike.ride()

city_factory = CityTransportFactory()
mountain_factory = MountainTransportFactory()

print("City Transport:")
print(get_transport(city_factory))

print("\nMountain Transport:")
print(get_transport(mountain_factory))
