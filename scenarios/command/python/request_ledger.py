# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
import threading
from concurrent.futures import Future

class RequestLedger:
    def __init__(self):
        self.lock = threading.Lock()
        self.pending = {}   # id -> Future
    
    def get_response_future(self, corr_id):
        print("pre-lock GRF")
        with self.lock:
            # corr_id = b'c366c131-23b1-4f4c-b0e8-f54a4c0cb664'
            print("New response future")
            response_future = Future()
            self.pending[corr_id] = response_future
            print(corr_id)
            print("put result in dict")
        return response_future

    def respond_to_request(self, corr_id, value):
        print("pre-lock R2R")
        with self.lock:
            # corr_id = b'c366c131-23b1-4f4c-b0e8-f54a4c0cb664'
            print("Respnding!")
            self.pending[corr_id].set_result(value)