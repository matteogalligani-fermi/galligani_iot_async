import asyncio
import random

class Broker:
    led = "OFF"
    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port
    async def esegui_comando(self, comando, writer, indirizzo):
        if comando.startswith("TEMP"):
            temp=round(random.uniform(0.0,40.0),1)
            ris=f"OK temp {temp} C\n"
            writer.write(ris.encode())
            await writer.drain()
        elif comando.startswith("UMIDITA"):
            um=random.randint(0,100)
            ris=f"OK umidita {um} %\n"
            writer.write(ris.encode())
            await writer.drain()
        elif comando.startswith("LED ON"):
            Broker.led = "ON"
            ris="OK led ON\n"
            writer.write(ris.encode())
            await writer.drain()
        elif comando.startswith("LED OFF"):
            Broker.led = "OFF"
            ris="OK led OFF\n"
            writer.write(ris.encode())
            await writer.drain()
        elif comando.startswith("STATO"):
            temp = round(random.uniform(0.0, 40.0),1)
            um = random.randint(0, 100)
            ris=f"OK temp {temp} C - umidita {um} % - LED {Broker.led}\n"
            writer.write(ris.encode())
            await writer.drain()
        elif comando.startswith("QUIT"):
            print(f"disconnessione {indirizzo}")
            writer.close()
            await writer.wait_closed()
        else:
            ris="ERR comando non riconosciuto"
            print(ris.encode())

    async def gestisci_client(self, reader, writer):
        indirizzo = writer.get_extra_info("peername")
        print(f"[CONNESSIONE] {indirizzo}")

        try:
            while True:
                dati = await reader.readline()
                if not dati:
                    break
                comando = dati.decode().strip()
                print(f"[RICEVUTO] {comando} da {indirizzo}")
                await self.esegui_comando(comando, writer, indirizzo)
        except ConnectionError:
            pass

    async def avvia(self):
        server = await asyncio.start_server(self.gestisci_client, self.host, self.port)
        print(f"[BROKER] In ascolto su {self.host}:{self.port}")
        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    broker = Broker()
    try:
        asyncio.run(broker.avvia())
    except KeyboardInterrupt:
        print("[STOP] Broker interrotto")