# Vehicle Sales Manager

A console application for managing vehicle stock across a dealership's branches: adding vehicles, viewing and searching stock, and processing purchase offers.

Originally written as a university coursework project while learning Python and object-oriented programming; since restructured into a proper multi-module package with clearer separation of concerns.

## Features

- Add cars, vans and minibuses to stock, each with type-specific attributes (doors, load capacity, seats)
- View the full stock list
- Search by registration number, vehicle type, make, model, colour, price range, or branch
- Make an offer on a vehicle; offers at or above 1.5x cost are accepted and the vehicle is removed from stock
- Stock is persisted to a JSON file between sessions

## Design

The project is split into layers so that business rules, storage, and the console interface can each change independently:

```
vehicle_sales_manager/
    enums.py        Branch and VehicleType enumerations
    exceptions.py    Domain-specific exceptions
    models.py        Vehicle (abstract base class), Car, Van, Minibus
    repository.py    VehicleRepository: in-memory stock plus JSON persistence
    cli.py           VehicleSalesApp: the menu-driven console interface
main.py              Entry point
tests/                Unit tests for models and the repository
```

`Vehicle` is an abstract base class defining shared, validated attributes (registration number, make, model, colour, price, cost, branch) and the interface every vehicle type must implement (`vehicle_type`, `_extra_fields`). `Car`, `Van`, and `Minibus` extend it with their own attributes and validation.

`VehicleRepository` owns the in-memory collection and is the only place that touches the filesystem, serialising vehicles to and from JSON. `VehicleSalesApp` handles all user input and output and delegates every business decision to the model and repository layers.

## Requirements

Python 3.9 or later. No external dependencies.

## Usage

```
python main.py
```

Stock is saved to `vehicles.json` in the working directory on exit, and loaded from there automatically on startup.

## Running the tests

```
python -m unittest discover
```
