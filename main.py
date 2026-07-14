"""Entry point for the UWS Vehicle Sales console application."""

from vehicle_sales_manager.cli import VehicleSalesApp


def main() -> None:
    app = VehicleSalesApp.with_default_storage()
    app.run()


if __name__ == "__main__":
    main()
