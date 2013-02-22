/* Author:

*/





//Array helpers
Array.prototype.getObjectById = function (obj) {
  var i = this.length;
  while (i--) {
      if (this[i].id + "" == obj + "") {
          return this[i];
      }
  }
  return null;
};

Array.prototype.getIndexById = function (obj) {
  var i = this.length;
  while (i--) {
      if (this[i].id + "" == obj + "") {
          return i;
      }
  }
  return -1;
};