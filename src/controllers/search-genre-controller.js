const { getAllPodcasts, getDistinctGenres, getPodcastsByGenre } = require('../services/firestoreService');
const predictPodcastRecommendations = require('../services/inferenceService');
const crypto = require('crypto');

async function postSearchHandler(request, h) {
  const { searchString } = request.payload;
  const { model } = request.server.app;

  if (!searchString) {
    return h.response({ error: 'searchString is required' }).code(400);
  }

  try {
    const recommendations = await predictPodcastRecommendations(model, searchString);
    const id = crypto.randomUUID();
    const createdAt = new Date().toISOString();

    const data = {
      id: id,
      recommendations: recommendations,
      createdAt: createdAt,
    };

    const response = h.response({
      status: 'success',
      message: 'Recommendations retrieved successfully.',
      data,
    });
    response.code(201);
    return response;
  } catch (error) {
    return h.response({ error: error.message }).code(500);
  }
}

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
    const podcastData = doc.data();
    return h.response({
      status: 'success',
      data: podcastData,
    }).code(200);
  } catch (error) {
    return h.response({ error: error.message }).code(500);
  }
}



module.exports = {
  postSearchHandler,
  getAllPodcastHandler,
  getGenrePodcastHandler,
  getPodcastByGenreHandler,
  getPodcastByIdHandler,
};
