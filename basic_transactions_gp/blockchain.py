# Paste your version of blockchain.py from the basic_block_gp
# folder here
import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)
    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }
        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
        self.chain.append(block)
        # Return the new block
        return block
    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block
        :param block": <dict> Block
        "return": <str>
        """
        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It convertes the string to bytes.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes
        # TODO: Create the block_string
        string_object = json.dumps(block, sort_keys=True).encode()
        # TODO: Hash this string using sha256
        raw_hash = hashlib.sha256(string_object)
        hex_hash = raw_hash.hexdigest()
        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand
        # TODO: Return the hashed block string in hexadecimal format
        return hex_hash
    @property
    def last_block(self):
        return self.chain[-1]
    
    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        guess = f"{block_string}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        # CHANGE VALID_PROOF TO REQUIRE 6 LEADING ZEROES
        return guess_hash[:6] == "000000"
# Instantiate our Node
app = Flask(__name__)
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')
# Instantiate the Blockchain
blockchain = Blockchain()

# MODIFY THE MINE ENDPOINT TO INSTEAD RECEIVE AND VALIDATE OR REJECT A NEW PROOF SENT BY A CLIENT
# IT SHOULD ACCEPT A POST
@app.route('/mine', methods=['POST'])
def mine():
    # USE data = request.get_json() TO PULL DATA OUT OF THE POST
    data = request.get_json()
    proof = data['proof']
    bId = data['id']

    if proof and bId:
        previous_hash = blockchain.hash(blockchain.last_block)
        block_string = json.dumps(blockchain.last_block, sort_keys=True)
        if blockchain.valid_proof(block_string, proof):
            blockchain.new_block(proof, previous_hash)
            response = {
                'message': 'New Block Forged',
            }
            return jsonify(response), 200
        else:
            response = {
                'message': 'Not valid',
            }
            return jsonify(response), 200  
        
    else:
        response = {
            'message': 'proof or id are not present'
        }
        return jsonify(response), 400

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'length': len(blockchain.chain),
        'chain': blockchain.chain
    }
    return jsonify(response), 200

# ADD AN ENDPOINT CALLED LAST_BLOCK THAT RETURNS THE LAST BLOCK IN THE CHAIN
@app.route('/last_block', methods=['GET'])
def last_block():
    last_b = blockchain.last_block
    response = {
        'last_block': last_b
    }
    return jsonify(response), 200

# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
