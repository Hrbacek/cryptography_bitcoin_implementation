from ECDSA.helper import hash256, read_varint
from script.Script import Script

class Transaction:
    def __init__(self, version, inputs, outputs, locktime, testnet=False):
        self.version = version
        self.inputs = inputs
        self.outputs = outputs
        self.locktime = locktime
        self.testnet = testnet
    
    def __repr__(self):
        tx_ins = ""
        for tx_in in self.inputs:
            tx_ins += tx_in.__repr__() + '\n'
        
        tx_outs = ""
        for tx_out in self.outputs:
            tx_outs += tx_out.__repr__() + '\n'
        
        return "tx: {}\nversion: {}\ninputs:\n{}outputs:\n{}locktime: {}".format(
            self.id(), self.version, tx_ins, tx_outs, self.locktime
        )
    
    def id(self):
        return self.hash().hex()

    def hash(self):
        return hash256(self.serialize())[::-1]
    
    @classmethod
    def parse(cls, s, testnet=False):
        version = int.from_bytes(s.read(4), "little")
        num_inputs = read_varint(s)
        inputs = [Input.parse(s) for _ in range(num_inputs)]
        num_outputs = read_varint(s)
        outputs = [Output.parse(s) for _ in range(num_outputs)]
        locktime = int.from_bytes(s.read(4), "little")
        return cls(version, inputs, outputs, locktime, testnet=testnet)
    
    def fee(self, testnet=False):
        input_sum, output_sum = 0, 0
        for tx_in in self.tx_ins:
            input_sum += tx_in.value(testnet=testnet)
        for tx_out in self.tx_outs:
            output_sum += tx_out.amount
        return input_sum - output_sum
    
    def serialize(self):
        result = self.version.to_bytes(4, "little")
        result += len(self.inputs).to_bytes(1, "little")
        for tx_in in self.inputs:
            result += tx_in.serialize()
        result += len(self.outputs).to_bytes(1, "little")
        for tx_out in self.outputs:
            result += tx_out.serialize()
        result += self.locktime.to_bytes(4, "little")
        return result

class Input:
    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence
    
    def __repr__(self):
        return "{}:{}".format(self.prev_tx.hex(), self.prev_index)

    
    @classmethod
    def parse(cls, s):
        prev_tx = s.read(32)[::-1]
        prev_index = int.from_bytes(s.read(4), "little")
        script_sig = Script.parse(s)
        sequence = int.from_bytes(s.read(4), "little")
        return cls(prev_tx, prev_index, script_sig, sequence)
    
    def serialize(self):
        result = self.prev_tx[::-1]
        result += self.prev_index.to_bytes(4, "little")
        result += self.script_sig.serialize()
        result += self.sequence.to_bytes(4, "little")
        return result

class Output:
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey
    
    def __repr__(self):
        return "{}:{}".format(self.amount, self.script_pubkey)

    @classmethod
    def parse(cls, s):
        amount = int.from_bytes(s.read(8), "little")
        script_pubkey = Script.parse(s)
        return cls(amount, script_pubkey)

    def serialize(self):
        result = self.amount.to_bytes(8, "little")
        result += self.script_pubkey.serialize()
        return result
    