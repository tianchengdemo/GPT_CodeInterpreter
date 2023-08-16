import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import uuid

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    name = str(uuid.uuid4().hex)
    while True:
        input_str = input('You: ')
        if input_str == 'exit':
            break
        responses = stub.SayHello(helloworld_pb2.HelloRequest(name=name, message=input_str))
        print('Bot: ', end='')
        for response in responses:
            print(response.message, end='', flush=True)
        print()
    
    responses = stub.SayHello(helloworld_pb2.HelloRequest(name=name, message='exit'))

if __name__ == '__main__':
    run()
