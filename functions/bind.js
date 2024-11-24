export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);
  const userId = url.searchParams.get("userId"); // Roblox userId from query
  const apiKey = url.searchParams.get("apiKey"); // API key entered by the user

  // Validate inputs
  if (!userId || !apiKey) {
    return new Response('Both userId and apiKey are required', { status: 400 });
  }

  // Simulate checking if the API key is valid
  const validApiKeys = await checkIfApiKeyExists(apiKey);
  if (!validApiKeys) {
    return new Response('Invalid API key', { status: 404 });
  }

  // Bind the key to the Roblox user (in this case, just storing it in memory or a simulated database)
  const result = await bindApiKeyToUser(userId, apiKey);

  // Return the result
  if (result) {
    return new Response('API key successfully bound to user.', {
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } else {
    return new Response('Failed to bind API key to user.', { status: 500 });
  }
}

// Simulate checking if the API key is valid (replace with real validation logic)
async function checkIfApiKeyExists(apiKey) {
  const validKeys = ['key-123456-abcdefg', 'key-789012-zyxwvut']; // Example valid keys
  return validKeys.includes(apiKey);
}

// Simulate binding the API key to a Roblox user (in memory or use a database)
async function bindApiKeyToUser(userId, apiKey) {
  // Example of what this might look like in a simulated database
  const userKeys = {
    '123456': ['key-123456-abcdefg'], // UserID 123456 has this key
    '789012': ['key-789012-zyxwvut'],
  };

  // Check if user exists, if not, create new entry
  if (!userKeys[userId]) {
    userKeys[userId] = [];
  }

  // Bind the API key to the user
  if (!userKeys[userId].includes(apiKey)) {
    userKeys[userId].push(apiKey);
    return true; // Successfully bound the key
  }

  return false; // Key already bound
}
