export async function onRequest(context) {
  const { request } = context;

  // Check if the request method is GET
  if (request.method === 'GET') {
    // Generate a simple API key (you can customize this generation logic)
    const apiKey = generateApiKey();

    // Return the API key in a JSON response
    return new Response(
      JSON.stringify({ apiKey }),
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
  } else {
    // Return a 404 if method is not GET
    return new Response('Not Found', { status: 404 });
  }
}

// Function to generate a simple API key (adjust as needed)
function generateApiKey() {
  return Math.random().toString(36).substring(2, 15);
}
