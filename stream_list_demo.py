"""Demo of streaming list."""

import sys
import grpc
import stream_list_pb2
import stream_list_pb2_grpc


def main() -> None:
  print(len(sys.argv))
  if len(sys.argv) > 3:
    print("ERROR")
    return

  creds = grpc.ssl_channel_credentials()
  with grpc.secure_channel(
      "dns:///youtube.googleapis.com:443", creds
  ) as channel:
    stub = stream_list_pb2_grpc.V3DataLiveChatMessageServiceStub(channel)
    # Uncomment one of the following authentication options:
    #
    # Using an API key
    metadata = (("x-goog-api-key", sys.argv[1]),)
    # Using an OAuth 2.0 access token
    # metadata = (("authorization", "Bearer " + sys.argv[1]),)
    next_page_token = None
    while True:
      request = stream_list_pb2.LiveChatMessageListRequest(
          part=["snippet","authorDetails"],
          live_chat_id=sys.argv[2],
          max_results=20,
          page_token=next_page_token,
      )
      for response in stub.StreamList(request, metadata=metadata):
        print(response)
        next_page_token = response.next_page_token
        if not next_page_token:
          break
        if response.offline_at:
          print("Stream End")
          return


if __name__ == "__main__":
  main()
