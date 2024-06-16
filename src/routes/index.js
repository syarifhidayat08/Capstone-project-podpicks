const firebaseAuthController = require('../controllers/firebase-auth-controller');
const {
  postSearchHandler,
  getAllPodcastHandler,
  getGenrePodcastHandler,
  getPodcastByGenreHandler,
  getPodcastByIdHandler
} = require('../controllers/search-genre-controller');

const routes = [
  {
    method: 'POST',
    path: '/api/register',
    handler: firebaseAuthController.registerUser,
  },
  {
    method: 'POST',
    path: '/api/login',
    handler: firebaseAuthController.loginUser,
  },
  {
    method: 'POST',
    path: '/api/logout',
    handler: firebaseAuthController.logoutUser,
  },
  {
    method: 'POST',
    path: '/api/reset-password',
    handler: firebaseAuthController.resetPassword,
  },
  {
    path: '/namesearch',
    method: 'POST',
    handler: postSearchHandler,
  },
  {
    path: '/podcasts',
    method: 'GET',
    handler: getAllPodcastHandler,
  },
  {
    path: '/podcasts/genres',
    method: 'GET',
    handler: getGenrePodcastHandler,
  },
  {
    path: '/podcasts/genres/{genre}',
    method: 'GET',
    handler: getPodcastByGenreHandler,
  },
  {
    path: '/podcasts/{id}',
    method: 'GET',
    handler: getPodcastByIdHandler,
  },
];

module.exports = routes;
