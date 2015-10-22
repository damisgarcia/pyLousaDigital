'use strict';

describe('Controller: MediaUploadCtrl', function () {

  // load the controller's module
  beforeEach(module('pyLousaDigitalApp'));

  var MediaUploadCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    MediaUploadCtrl = $controller('MediaUploadCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(MediaUploadCtrl.awesomeThings.length).toBe(3);
  });
});
