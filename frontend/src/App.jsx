import Form from "./components/Form";
import useDecodedPayload from "./components/Decoder";

function App() {
  const decodedPayload = useDecodedPayload();

  return (
    <div>
      {decodedPayload.tenantId ? (
        <Form {...decodedPayload} />
      ) : (
        <h1>Page cannot be loaded</h1>
      )}
    </div>
  );
}

export default App;
