const firebaseAuthController = require('../controllers/firebase-auth-controller');
const {
  getAllPodcastHandler,
  getGenrePodcastHandler,
  getPodcastByGenreHandler,
  getPodcastByIdHandler
} = require('../controllers/search-genre-controller');
const { addBookmark, removeBookmark, getUserBookmarks } = require('../controllers/bookmark-controller');
const verifyToken = require('../middleware/index');


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
  {
    method: 'POST',
    path: '/api/bookmarks',
    handler: addBookmark,
    options: {
      pre: [{ method: verifyToken }],
    },
  },
  {
    method: 'DELETE',
    path: '/api/bookmarks',
    handler: removeBookmark,
    options: {
      pre: [{ method: verifyToken }],
    },
  },
  {
    method: 'GET',
    path: '/api/bookmarks/{userId}',
    handler: getUserBookmarks,
    options: {
      pre: [{ method: verifyToken }],
    },
  },
];

module.exports = routes;
