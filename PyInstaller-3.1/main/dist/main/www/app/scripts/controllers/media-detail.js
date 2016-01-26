'use strict';

/**
 * @ngdoc function
 * @name pyLousaDigitalApp.controller:MediaDetailCtrl
 * @description
 * # MediaDetailCtrl
 * Controller of the pyLousaDigitalApp
 */
angular.module('pyLousaDigitalApp',[])
  .controller('MediaDetailCtrl', function ($scope,$location) {
    this.media = $location.search()
    var video = document.getElementById('player')
    video.poster = this.media.thumbnail
    video.src = this.media.url
  });
