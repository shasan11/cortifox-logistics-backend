from master.models import MasterData

def populate_demo_data():
    demo_data = [
        {"type_master": "INCO", "name": "FOB", "description": "Free on Board"},
        {"type_master": "INCO", "name": "CIF", "description": "Cost, Insurance and Freight"},
        {"type_master": "INCO", "name": "EXW", "description": "Ex Works"},
        {"type_master": "INCO", "name": "DAP", "description": "Delivered at Place"},
        {"type_master": "INCO", "name": "DDP", "description": "Delivered Duty Paid"},
        {"type_master": "INCO", "name": "FCA", "description": "Free Carrier"},

        {"type_master": "STATUS", "name": "Pending", "description": "Shipment is pending"},
        {"type_master": "STATUS", "name": "In Transit", "description": "Shipment is in transit"},
        {"type_master": "STATUS", "name": "Delivered", "description": "Shipment has been delivered"},
        {"type_master": "STATUS", "name": "Cancelled", "description": "Shipment has been cancelled"},
        {"type_master": "STATUS", "name": "Delayed", "description": "Shipment has been delayed"},
        {"type_master": "STATUS", "name": "Returned", "description": "Shipment has been returned"},

        {"type_master": "CONTAINER_TYPE", "name": "Dry Container", "description": "Standard shipping container for dry goods"},
        {"type_master": "CONTAINER_TYPE", "name": "Reefer Container", "description": "Refrigerated shipping container"},
        {"type_master": "CONTAINER_TYPE", "name": "Open Top Container", "description": "Container with an open roof"},
        {"type_master": "CONTAINER_TYPE", "name": "Flat Rack Container", "description": "Container for oversized cargo"},
        {"type_master": "CONTAINER_TYPE", "name": "ISO Tank", "description": "Container for liquids"},
        {"type_master": "CONTAINER_TYPE", "name": "High Cube Container", "description": "Tall container for large cargo"},

        {"type_master": "CARGO_TYPE", "name": "General Cargo", "description": "Standard cargo items"},
        {"type_master": "CARGO_TYPE", "name": "Perishable Goods", "description": "Temperature-sensitive cargo"},
        {"type_master": "CARGO_TYPE", "name": "Hazardous Materials", "description": "Cargo that requires special handling"},
        {"type_master": "CARGO_TYPE", "name": "Oversized Cargo", "description": "Cargo that exceeds standard dimensions"},
        {"type_master": "CARGO_TYPE", "name": "Fragile Goods", "description": "Delicate items requiring careful handling"},
        {"type_master": "CARGO_TYPE", "name": "Valuable Cargo", "description": "High-value goods"},

        {"type_master": "TRAILER_TYPE", "name": "Flatbed Trailer", "description": "Open trailer for oversized items"},
        {"type_master": "TRAILER_TYPE", "name": "Refrigerated Trailer", "description": "Trailer for temperature-controlled goods"},
        {"type_master": "TRAILER_TYPE", "name": "Dry Van Trailer", "description": "Enclosed trailer for standard cargo"},
        {"type_master": "TRAILER_TYPE", "name": "Lowboy Trailer", "description": "Trailer for very tall items"},
        {"type_master": "TRAILER_TYPE", "name": "Tanker Trailer", "description": "Trailer for liquid cargo"},
        {"type_master": "TRAILER_TYPE", "name": "Extendable Trailer", "description": "Trailer for long items"},

        {"type_master": "DELIVERY_TYPE", "name": "Door to Door", "description": "Pickup and delivery at specified addresses"},
        {"type_master": "DELIVERY_TYPE", "name": "Port to Door", "description": "Delivery from port to address"},
        {"type_master": "DELIVERY_TYPE", "name": "Door to Port", "description": "Pickup from address to port"},
        {"type_master": "DELIVERY_TYPE", "name": "Port to Port", "description": "Shipment between two ports"},
        {"type_master": "DELIVERY_TYPE", "name": "Expedited Delivery", "description": "Faster delivery service"},
        {"type_master": "DELIVERY_TYPE", "name": "Standard Delivery", "description": "Regular delivery service"},

        {"type_master": "ShipmenSubType", "name": "Full Container Load", "description": "Cargo that occupies the entire container"},
        {"type_master": "ShipmenSubType", "name": "Less Than Container Load", "description": "Cargo sharing a container with others"},
        {"type_master": "ShipmenSubType", "name": "Express", "description": "Fast shipment service"},
        {"type_master": "ShipmenSubType", "name": "Economy", "description": "Cost-effective shipment"},
        {"type_master": "ShipmenSubType", "name": "Break Bulk", "description": "Loose cargo not containerized"},
        {"type_master": "ShipmenSubType", "name": "Project Cargo", "description": "Special cargo for specific projects"}
    ]

    for data in demo_data:
        MasterData.objects.create(**data)

# Run the script
populate_demo_data()
