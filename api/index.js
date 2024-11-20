export default {
    async fetch(request) {
        return new Response('Hello, World from GitHub!', {
            headers: { 'content-type': 'text/plain' },
        });
    },
};
