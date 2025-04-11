"use strict";
/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
exports.id = "vendor-chunks/node-domexception";
exports.ids = ["vendor-chunks/node-domexception"];
exports.modules = {

/***/ "(rsc)/./node_modules/node-domexception/index.js":
/*!*************************************************!*\
  !*** ./node_modules/node-domexception/index.js ***!
  \*************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

eval("\n\n/*! node-domexception. MIT License. Jimmy Wärting <https://jimmy.warting.se/opensource> */\n\nif (!globalThis.DOMException) {\n  try {\n    const {\n        MessageChannel\n      } = __webpack_require__(/*! worker_threads */ \"worker_threads\"),\n      port = new MessageChannel().port1,\n      ab = new ArrayBuffer();\n    port.postMessage(ab, [ab, ab]);\n  } catch (err) {\n    err.constructor.name === 'DOMException' && (globalThis.DOMException = err.constructor);\n  }\n}\nmodule.exports = globalThis.DOMException;//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKHJzYykvLi9ub2RlX21vZHVsZXMvbm9kZS1kb21leGNlcHRpb24vaW5kZXguanMiLCJtYXBwaW5ncyI6Ijs7QUFBQTs7QUFFQSxJQUFJLENBQUNBLFVBQVUsQ0FBQ0MsWUFBWSxFQUFFO0VBQzVCLElBQUk7SUFDRixNQUFNO1FBQUVDO01BQWUsQ0FBQyxHQUFHQyxtQkFBTyxDQUFDLHNDQUFnQixDQUFDO01BQ3BEQyxJQUFJLEdBQUcsSUFBSUYsY0FBYyxDQUFDLENBQUMsQ0FBQ0csS0FBSztNQUNqQ0MsRUFBRSxHQUFHLElBQUlDLFdBQVcsQ0FBQyxDQUFDO0lBQ3RCSCxJQUFJLENBQUNJLFdBQVcsQ0FBQ0YsRUFBRSxFQUFFLENBQUNBLEVBQUUsRUFBRUEsRUFBRSxDQUFDLENBQUM7RUFDaEMsQ0FBQyxDQUFDLE9BQU9HLEdBQUcsRUFBRTtJQUNaQSxHQUFHLENBQUNDLFdBQVcsQ0FBQ0MsSUFBSSxLQUFLLGNBQWMsS0FDckNYLFVBQVUsQ0FBQ0MsWUFBWSxHQUFHUSxHQUFHLENBQUNDLFdBQVcsQ0FDMUM7RUFDSDtBQUNGO0FBRUFFLE1BQU0sQ0FBQ0MsT0FBTyxHQUFHYixVQUFVLENBQUNDLFlBQVkiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9waW5lbGFuZHMtd2lsZGZpcmUtYXBwLy4vbm9kZV9tb2R1bGVzL25vZGUtZG9tZXhjZXB0aW9uL2luZGV4LmpzP2FlMGEiXSwic291cmNlc0NvbnRlbnQiOlsiLyohIG5vZGUtZG9tZXhjZXB0aW9uLiBNSVQgTGljZW5zZS4gSmltbXkgV8OkcnRpbmcgPGh0dHBzOi8vamltbXkud2FydGluZy5zZS9vcGVuc291cmNlPiAqL1xuXG5pZiAoIWdsb2JhbFRoaXMuRE9NRXhjZXB0aW9uKSB7XG4gIHRyeSB7XG4gICAgY29uc3QgeyBNZXNzYWdlQ2hhbm5lbCB9ID0gcmVxdWlyZSgnd29ya2VyX3RocmVhZHMnKSxcbiAgICBwb3J0ID0gbmV3IE1lc3NhZ2VDaGFubmVsKCkucG9ydDEsXG4gICAgYWIgPSBuZXcgQXJyYXlCdWZmZXIoKVxuICAgIHBvcnQucG9zdE1lc3NhZ2UoYWIsIFthYiwgYWJdKVxuICB9IGNhdGNoIChlcnIpIHtcbiAgICBlcnIuY29uc3RydWN0b3IubmFtZSA9PT0gJ0RPTUV4Y2VwdGlvbicgJiYgKFxuICAgICAgZ2xvYmFsVGhpcy5ET01FeGNlcHRpb24gPSBlcnIuY29uc3RydWN0b3JcbiAgICApXG4gIH1cbn1cblxubW9kdWxlLmV4cG9ydHMgPSBnbG9iYWxUaGlzLkRPTUV4Y2VwdGlvblxuIl0sIm5hbWVzIjpbImdsb2JhbFRoaXMiLCJET01FeGNlcHRpb24iLCJNZXNzYWdlQ2hhbm5lbCIsInJlcXVpcmUiLCJwb3J0IiwicG9ydDEiLCJhYiIsIkFycmF5QnVmZmVyIiwicG9zdE1lc3NhZ2UiLCJlcnIiLCJjb25zdHJ1Y3RvciIsIm5hbWUiLCJtb2R1bGUiLCJleHBvcnRzIl0sInNvdXJjZVJvb3QiOiIifQ==\n//# sourceURL=webpack-internal:///(rsc)/./node_modules/node-domexception/index.js\n");

/***/ })

};
;