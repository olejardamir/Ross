class EchoController:
    def process_echo(self, body: dict) -> str:
        if "data" in body:
            return "data exists"
        return "data not found"
