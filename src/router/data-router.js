const express = require('express');
const dataRouter = express.Router();
const data_controller = require('../controller/data-controller');

dataRouter.get('/data_get', data_controller.data_get);

module.exports = dataRouter;
