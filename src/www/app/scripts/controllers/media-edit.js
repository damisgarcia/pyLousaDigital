'use strict';

/**
 * @ngdoc function
 * @name pyLousaDigitalApp.controller:MediaEditCtrl
 * @description
 * # MediaEditCtrl
 * Controller of the pyLousaDigitalApp
 */
angular.module('pyLousaDigitalApp')
  .controller('MediaEditCtrl', function ($scope,$stateParams) {
    $scope.media = $scope.repository.thumbnails[$stateParams.id]
    $scope.media.$id = $stateParams.id
    $scope.media.new_name = $scope.media.name
  });
