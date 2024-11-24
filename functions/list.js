const validApiKeys = {};  // This object stores the API keys for users

// Simulate API key generation (this would be part of your key generation logic)
function generateApiKey(userId) {
  const apiKey = `key-${userId}-${Math.random().toString(36).substr(2, 9)}`;
  validApiKeys[userId] = apiKey; // Store the generated key for binding
  return apiKey;
}

export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);
  
  // If the user accesses the /list-keys endpoint, return the list of keys
  if (url.pathname === "/list-keys") {
    const apiKeyList = Object.keys(validApiKeys).map(userId => ({
      userId: userId,
      apiKey: validApiKeys[userId]
    }));

    // Return the list of API keys in JSON format
    return new Response(JSON.stringify(apiKeyList), {
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Default response if the URL doesn't match /list-keys
  return new Response("Not Found", { status: 404 });
}
