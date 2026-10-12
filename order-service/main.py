"""
order-service: the Week 2 service, now with a database connectivity check.

You do not need to change this file. Your job this week is to write the
compose.yaml that runs this service together with a Postgres database and
wires the two together. See the assignment handout on D2L.

The /db-check route is how you prove your Compose networking works: it tries
to open a TCP connection to DB_HOST on the Postgres port and reports back.
"""
import os
import socket

from fastapi import FastAPI

app = FastAPI(title="order-service")

DB_HOST = os.environ.get("DB_HOST", "not-set")
DB_PORT = int(os.environ.get("DB_PORT", "5432"))

ORDERS = [
    {"id": 1, "item": "widget", "qty": 3},
    {"id": 2, "item": "gadget", "qty": 1},
]


@app.get("/health")
def health():
    """Liveness check. The container is running if this returns ok."""
    return {"status": "ok"}


@app.get("/orders")
def list_orders():
    """Return all orders."""
    return {"orders": ORDERS}


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    """Return a single order by id."""
    for order in ORDERS:
        if order["id"] == order_id:
            return order
    return {"error": "order not found", "id": order_id}


@app.get("/db-check")
def db_check():
    """
    Try to open a TCP connection to DB_HOST:DB_PORT.

    reachable=true means this container resolved the hostname in DB_HOST and
    something accepted a connection on that port. That is exactly what you are
    proving in this week's lab.
    """
    try:
        with socket.create_connection((DB_HOST, DB_PORT), timeout=2):
            return {"db_host": DB_HOST, "db_port": DB_PORT, "reachable": True}
    except socket.gaierror:
        return {
            "db_host": DB_HOST,
            "db_port": DB_PORT,
            "reachable": False,
            "error": "hostname could not be resolved: check that DB_HOST matches your service name",
        }
    except (socket.timeout, OSError) as exc:
        return {
            "db_host": DB_HOST,
            "db_port": DB_PORT,
            "reachable": False,
            "error": f"could not connect: {exc}",
        }
