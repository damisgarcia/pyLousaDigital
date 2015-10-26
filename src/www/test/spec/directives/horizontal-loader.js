'use strict';

describe('Directive: horizontalLoader', function () {

  // load the directive's module
  beforeEach(module('pyLousaDigitalApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<horizontal-loader></horizontal-loader>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the horizontalLoader directive');
  }));
});
