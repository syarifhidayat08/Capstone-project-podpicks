const { Firestore } = require('@google-cloud/firestore');

const firestore = new Firestore();

async function getAllPodcasts() {
    const snapshot = await firestore.collection('podcast_data').get();
    return snapshot.docs.map(doc => {
        return { id: doc.id, ...doc.data() }; 
    });
}

async function getPodcastsByGenre(genre) {
    const snapshot = await firestore.collection('podcast_data').where('Genre', '==', genre).get();
    return snapshot.docs.map(doc => {
        return { id: doc.id, ...doc.data() }; 
    });
}

async function getDistinctGenres() {
    const snapshot = await firestore.collection('podcast_data').get();
    const genres = new Set();
    snapshot.docs.forEach(doc => {
        genres.add(doc.data().Genre);
    });
    return Array.from(genres);
}

module.exports = {
    getAllPodcasts,
    getDistinctGenres,
    getPodcastsByGenre,
};