from circuitbreaker import CircuitBreakerMonitor
from fastapi import HTTPException


class backoff_handlers:

    def backoff_hdlr(details):
        print("Backing off {wait:0.1f} seconds after {tries} tries "
              "calling function {target}".format(**details))


class circuit_handlers:

    @staticmethod
    def circuit_hdlr():
        for x in CircuitBreakerMonitor.get_circuits():
            msg = "name:{}. state: {}. open_remaining: {}. open_until:{}. failure_count: {}"

            return msg.format(x.name, x.state, x.open_remaining, x.open_until, x.failure_count)

    def exception_condition(thrown_type, thrown_value):
        return issubclass(thrown_type, HTTPException) and thrown_value.status_code == 400

    @staticmethod
    def fallback_response():
        raise HTTPException(status_code=503, detail="Service Unavailable, please try again later")
