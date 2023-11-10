import unittest
import time

from UPISAS import get_response_for_get_request
from UPISAS.exemplars.your_exemplar import YourExemplar
from UPISAS.strategies.empty_strategy import EmptyStrategy


class TestYourExemplarInterface(unittest.TestCase):

    def setUp(self):
        self.exemplar = YourExemplar(auto_start=True)
        self._start_server_and_wait_until_is_up()
        self.strategy = EmptyStrategy(self.exemplar)

    def tearDown(self):
        if self.exemplar and self.exemplar.exemplar_container:
            self.exemplar.stop_container()

    def test_get_adaptation_options_successfully(self):
        self.strategy.get_adaptation_options(with_validation=False)
        self.assertIsNotNone(self.strategy.knowledge.adaptation_options)

    def test_monitor_successfully(self):
        successful = self.strategy.monitor(with_validation=False)
        self.assertTrue(successful)
        self.assertNotEqual(self.strategy.knowledge.monitored_data, dict())

    def test_execute_successfully(self):
        successful = self.strategy.execute({"config": "|../repository/TCPNetwork.o,/home/roberto/dana//components/net/TCP.o,../repository/request/RequestHandlerPT.o,../repository/app_protocols/HTTPProtocol.o,../repository/http/HTTPHeader1_0.o,../repository/http/handler/GET/HTTPGETCMP.o,/home/roberto/dana//components/io/File.o,../repository/compression/ZLIB.o,/home/roberto/dana//components/os/Run.o,/home/roberto/dana//components/time/DateUtil.o,../repository/http/util/HTTPUtil.o,/home/roberto/dana//components/data/StringUtil.o,/home/roberto/dana//components/data/adt/List.o|0:net.TCPSocket:1,0:net.TCPServerSocket:1,0:request.RequestHandler:2,2:app_protocols.AppProtocol:3,3:http.HTTPHeader:4,4:http.handler.GET.HTTPGET:5,5:io.File:6,5:compression.Compression:7,7:os.Run:8,7:time.DateUtil:9,7:io.FileSystem:6,4:http.util.HTTPUtil:10,10:io.FileSystem:6,10:data.StringUtil:11,11:data.adt.List:12|"}, with_validation=False)
        self.assertTrue(successful)

    def test_adaptation_options_schema_endpoint_reachable(self):
        self.strategy.get_adaptation_options_schema()
        self.assertIsNotNone(self.strategy.knowledge.adaptation_options_schema)

    def test_monitor_schema_endpoint_reachable(self):
        self.strategy.get_monitor_schema()
        self.assertIsNotNone(self.strategy.knowledge.monitor_schema)

    def test_execute_schema_endpoint_reachable(self):
        self.strategy.get_execute_schema()
        self.assertIsNotNone(self.strategy.knowledge.execute_schema)

    def test_schema_of_adaptation_options(self):
        self.strategy.get_adaptation_options_schema()
        with self.assertLogs() as cm:
            self.strategy.get_adaptation_options()
            self.assertTrue("JSON object validated by JSON Schema" in ", ".join(cm.output))
        self.assertIsNotNone(self.strategy.knowledge.adaptation_options)

    def test_schema_of_monitor(self):
        self.strategy.get_monitor_schema()
        with self.assertLogs() as cm:
            successful = self.strategy.monitor()
            self.assertTrue("JSON object validated by JSON Schema" in ", ".join(cm.output))
        self.assertTrue(successful)
        self.assertNotEqual(self.strategy.knowledge.monitored_data, dict())

    def test_schema_of_execute(self):
        self.strategy.get_execute_schema()
        with self.assertLogs() as cm:
            successful = self.strategy.execute({"server_number": 2, "dimmer_factor": 0.5})
            self.assertTrue("JSON object validated by JSON Schema" in ", ".join(cm.output))
        self.assertTrue(successful)

    def _start_server_and_wait_until_is_up(self, base_endpoint="http://localhost:5001"):
        self.exemplar.start_run()
        while True:
            time.sleep(1)
            print("trying to connect...")
            response = get_response_for_get_request(base_endpoint)
            print(response.status_code)
            if response.status_code < 400:
                return


if __name__ == '__main__':
    unittest.main()
