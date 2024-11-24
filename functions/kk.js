// Simulate API Key generation logic
function generateApiKey(userId) {
  // Create a simple key based on userId (you could use a more secure method in production)
  return `key-${userId}-${Math.random().toString(36).substr(2, 9)}`;
}

export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);
  const userId = url.searchParams.get("userId");

  // Validate userId
  if (!userId) {
    return new Response('userId is required', { status: 400 });
  }

  // Generate an API key for the user
  const apiKey = generateApiKey(userId);

  // Respond with the API key
  return new Response(JSON.stringify({ apiKey }), {
    headers: { 'Content-Type': 'application/json' },
  });
}
