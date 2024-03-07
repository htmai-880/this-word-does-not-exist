import argparse
import grpc

from word_service_proto import wordservice_pb2
from word_service_proto import wordservice_pb2_grpc


def run(host, port, api_key, auth_token, timeout, use_tls, word, do_sample=False):
    if use_tls:
        with open("nginx.pem", "rb") as f:
            creds = grpc.ssl_channel_credentials(f.read())
        channel = grpc.secure_channel("{}:{}".format(host, port), creds)
    else:
        channel = grpc.insecure_channel("{}:{}".format(host, port))

    stub = wordservice_pb2_grpc.WordServiceStub(channel)
    metadata = []
    if api_key:
        metadata.append(("x-api-key", api_key))
    if auth_token:
        metadata.append(("authorization", "Bearer " + auth_token))

    req = wordservice_pb2.DefineWordRequest()
    req.word = word
    req.do_sample = do_sample
    try:
        response = stub.DefineWord(req, timeout, metadata=metadata)
    except Exception:
        print("Service raised exception")
        raise

    print(f"Define word response: {response}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--host", default="localhost", help="The host to connect to")
    parser.add_argument("--port", type=int, default=8000, help="The port to connect to")
    parser.add_argument("--timeout", type=int, default=10, help="The call timeout, in seconds")
    parser.add_argument("--api_key", default=None, help="The API key to use for the call")
    parser.add_argument("--auth_token", default=None, help="The JWT auth token to use for the call")
    parser.add_argument("--use_tls", type=bool, default=False, help="Enable when the server requires TLS")
    parser.add_argument("--word", type=str, default="fuddleduddle", help="The word to define")
    parser.add_argument("--do_sample", type=bool, default=False, help="Greedy generation or not.")
    args = parser.parse_args()
    run(args.host, args.port, args.api_key, args.auth_token, args.timeout, args.use_tls, args.word, args.do_sample)
