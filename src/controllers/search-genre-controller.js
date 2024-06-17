const { getAllPodcasts, getDistinctGenres, getPodcastsByGenre } = require('../services/firestoreService');

async function getAllPodcastHandler(request, h) {
  try {
    const podcasts = await getAllPodcasts();
    return h.response({
      status: 'success',
      data: podcasts,
    }).code(200);
  } catch (error) {
    return h.response({ error: error.message }).code(500);
  }
}

async function getGenrePodcastHandler(request, h) {
  try {
    const genres = await getDistinctGenres();
    return h.response({
      status: 'success',
      data: genres,
    }).code(200);
  } catch (error) {
    return h.response({ error: error.message }).code(500);
  }
}

async function getPodcastByGenreHandler(request, h) {
  const { genre } = request.params;
  try {
    const podcasts = await getPodcastsByGenre(genre);
    return h.response({
      status: 'success',
      data: podcasts,
    }).code(200);
  } catch (error) {
    return h.response({ error: error.message }).code(500);
  }
}

async function getPodcastByIdHandler(request, h) {
  const { id } = request.params;
  const { db } = request.server.app;

  try {
    const doc = await db.collection('podcast_data').doc(id).get();
    if (!doc.exists) {
      return h.response({ error: 'Podcast not found' }).code(404);
    }
    const podcastData = { id: doc.id, ...doc.data() }; 
    return h.response({
      status: 'success',
      data: podcastData,
    }).code(200);
  } catch (error) {
    return h.response({ error: error.message }).code(500);
  }
}

module.exports = {

  getAllPodcastHandler,
  getGenrePodcastHandler,
  getPodcastByGenreHandler,
  getPodcastByIdHandler,
};
