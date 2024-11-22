import { MongoClient } from 'mongodb';

const uri = process.env.MONGO_URI;  // Store this in Vercel's environment variables
const client = new MongoClient(uri);

export default async function handler(req, res) {
  if (req.method === 'POST') {
    try {
      const { data } = req.body;
      await client.connect();
      const database = client.db('your-db-name');
      const collection = database.collection('your-collection');
      const result = await collection.insertOne({ data });
      
      res.status(200).json({ success: true, insertedId: result.insertedId });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    } finally {
      await client.close();
    }
  } else {
    res.status(405).json({ success: false, message: 'Method not allowed' });
  }
}
