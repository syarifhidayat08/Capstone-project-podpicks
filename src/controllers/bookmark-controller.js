const { Firestore } = require('@google-cloud/firestore');

const firestore = new Firestore();

async function addBookmark(req, h) {
  const { podcastId } = req.payload;
  const userId = req.auth.credentials.uid;

  if (!userId || !podcastId) {
    return h.response({ error: 'userId and podcastId are required' }).code(400);
  }

  try {
    const bookmarkRef = firestore.collection('bookmarks').doc(userId);
    const doc = await bookmarkRef.get();

    if (!doc.exists) {
      await bookmarkRef.set({ podcasts: [podcastId] });
    } else {
      const bookmarks = doc.data().podcasts;
      if (!bookmarks.includes(podcastId)) {
        bookmarks.push(podcastId);
        await bookmarkRef.update({ podcasts: bookmarks });
      }
    }

    return h.response({ message: 'Bookmark added successfully' }).code(200);
  } catch (error) {
    console.error('Error adding bookmark:', error);
    return h.response({ error: error.message }).code(500);
  }
}

async function removeBookmark(req, h) {
  const { podcastId } = req.payload;
  const userId = req.auth.credentials.uid;

  if (!userId || !podcastId) {
    return h.response({ error: 'userId and podcastId are required' }).code(400);
  }

  try {
    const bookmarkRef = firestore.collection('bookmarks').doc(userId);
    const doc = await bookmarkRef.get();

    if (doc.exists) {
      const bookmarks = doc.data().podcasts;
      const index = bookmarks.indexOf(podcastId);
      if (index > -1) {
        bookmarks.splice(index, 1);
        await bookmarkRef.update({ podcasts: bookmarks });
      }
    }

    return h.response({ message: 'Bookmark removed successfully' }).code(200);
  } catch (error) {
    console.error('Error removing bookmark:', error);
    return h.response({ error: error.message }).code(500);
  }
}

async function getUserBookmarks(req, h) {
  const userId = req.auth.credentials.uid;

  if (!userId) {
    return h.response({ error: 'userId is required' }).code(400);
  }

  try {
    const bookmarkRef = firestore.collection('bookmarks').doc(userId);
    const doc = await bookmarkRef.get();

    if (doc.exists) {
      return h.response({ bookmarks: doc.data().podcasts }).code(200);
    } else {
      return h.response({ bookmarks: [] }).code(200);
    }
  } catch (error) {
    console.error('Error getting user bookmarks:', error);
    return h.response({ error: error.message }).code(500);
  }
}

module.exports = {
  addBookmark,
  removeBookmark,
  getUserBookmarks,
};