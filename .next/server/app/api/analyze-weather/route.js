"use strict";
/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
(() => {
var exports = {};
exports.id = "app/api/analyze-weather/route";
exports.ids = ["app/api/analyze-weather/route"];
exports.modules = {

/***/ "next/dist/compiled/next-server/app-route.runtime.dev.js":
/*!**************************************************************************!*\
  !*** external "next/dist/compiled/next-server/app-route.runtime.dev.js" ***!
  \**************************************************************************/
/***/ ((module) => {

module.exports = require("next/dist/compiled/next-server/app-route.runtime.dev.js");

/***/ }),

/***/ "fs":
/*!*********************!*\
  !*** external "fs" ***!
  \*********************/
/***/ ((module) => {

module.exports = require("fs");

/***/ }),

/***/ "http":
/*!***********************!*\
  !*** external "http" ***!
  \***********************/
/***/ ((module) => {

module.exports = require("http");

/***/ }),

/***/ "https":
/*!************************!*\
  !*** external "https" ***!
  \************************/
/***/ ((module) => {

module.exports = require("https");

/***/ }),

/***/ "node:fs":
/*!**************************!*\
  !*** external "node:fs" ***!
  \**************************/
/***/ ((module) => {

module.exports = require("node:fs");

/***/ }),

/***/ "node:stream":
/*!******************************!*\
  !*** external "node:stream" ***!
  \******************************/
/***/ ((module) => {

module.exports = require("node:stream");

/***/ }),

/***/ "node:stream/web":
/*!**********************************!*\
  !*** external "node:stream/web" ***!
  \**********************************/
/***/ ((module) => {

module.exports = require("node:stream/web");

/***/ }),

/***/ "path":
/*!***********************!*\
  !*** external "path" ***!
  \***********************/
/***/ ((module) => {

module.exports = require("path");

/***/ }),

/***/ "punycode":
/*!***************************!*\
  !*** external "punycode" ***!
  \***************************/
/***/ ((module) => {

module.exports = require("punycode");

/***/ }),

/***/ "stream":
/*!*************************!*\
  !*** external "stream" ***!
  \*************************/
/***/ ((module) => {

module.exports = require("stream");

/***/ }),

/***/ "url":
/*!**********************!*\
  !*** external "url" ***!
  \**********************/
/***/ ((module) => {

module.exports = require("url");

/***/ }),

/***/ "util":
/*!***********************!*\
  !*** external "util" ***!
  \***********************/
/***/ ((module) => {

module.exports = require("util");

/***/ }),

/***/ "worker_threads":
/*!*********************************!*\
  !*** external "worker_threads" ***!
  \*********************************/
/***/ ((module) => {

module.exports = require("worker_threads");

/***/ }),

/***/ "zlib":
/*!***********************!*\
  !*** external "zlib" ***!
  \***********************/
/***/ ((module) => {

module.exports = require("zlib");

/***/ }),

/***/ "(rsc)/./node_modules/next/dist/build/webpack/loaders/next-app-loader.js?name=app%2Fapi%2Fanalyze-weather%2Froute&page=%2Fapi%2Fanalyze-weather%2Froute&appPaths=&pagePath=private-next-app-dir%2Fapi%2Fanalyze-weather%2Froute.ts&appDir=%2Fapp%2Fapp&pageExtensions=tsx&pageExtensions=ts&pageExtensions=jsx&pageExtensions=js&rootDir=%2Fapp&isDev=true&tsconfigPath=tsconfig.json&basePath=&assetPrefix=&nextConfigOutput=&preferredRegion=&middlewareConfig=e30%3D!":
/*!*************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/next/dist/build/webpack/loaders/next-app-loader.js?name=app%2Fapi%2Fanalyze-weather%2Froute&page=%2Fapi%2Fanalyze-weather%2Froute&appPaths=&pagePath=private-next-app-dir%2Fapi%2Fanalyze-weather%2Froute.ts&appDir=%2Fapp%2Fapp&pageExtensions=tsx&pageExtensions=ts&pageExtensions=jsx&pageExtensions=js&rootDir=%2Fapp&isDev=true&tsconfigPath=tsconfig.json&basePath=&assetPrefix=&nextConfigOutput=&preferredRegion=&middlewareConfig=e30%3D! ***!
  \*************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   headerHooks: () => (/* binding */ headerHooks),\n/* harmony export */   originalPathname: () => (/* binding */ originalPathname),\n/* harmony export */   patchFetch: () => (/* binding */ patchFetch),\n/* harmony export */   requestAsyncStorage: () => (/* binding */ requestAsyncStorage),\n/* harmony export */   routeModule: () => (/* binding */ routeModule),\n/* harmony export */   serverHooks: () => (/* binding */ serverHooks),\n/* harmony export */   staticGenerationAsyncStorage: () => (/* binding */ staticGenerationAsyncStorage),\n/* harmony export */   staticGenerationBailout: () => (/* binding */ staticGenerationBailout)\n/* harmony export */ });\n/* harmony import */ var next_dist_server_future_route_modules_app_route_module_compiled__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! next/dist/server/future/route-modules/app-route/module.compiled */ \"(rsc)/./node_modules/next/dist/server/future/route-modules/app-route/module.compiled.js\");\n/* harmony import */ var next_dist_server_future_route_modules_app_route_module_compiled__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(next_dist_server_future_route_modules_app_route_module_compiled__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var next_dist_server_future_route_kind__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! next/dist/server/future/route-kind */ \"(rsc)/./node_modules/next/dist/server/future/route-kind.js\");\n/* harmony import */ var next_dist_server_lib_patch_fetch__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! next/dist/server/lib/patch-fetch */ \"(rsc)/./node_modules/next/dist/server/lib/patch-fetch.js\");\n/* harmony import */ var next_dist_server_lib_patch_fetch__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(next_dist_server_lib_patch_fetch__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var _app_app_api_analyze_weather_route_ts__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./app/api/analyze-weather/route.ts */ \"(rsc)/./app/api/analyze-weather/route.ts\");\n\n\n\n\n// We inject the nextConfigOutput here so that we can use them in the route\n// module.\nconst nextConfigOutput = \"\"\nconst routeModule = new next_dist_server_future_route_modules_app_route_module_compiled__WEBPACK_IMPORTED_MODULE_0__.AppRouteRouteModule({\n    definition: {\n        kind: next_dist_server_future_route_kind__WEBPACK_IMPORTED_MODULE_1__.RouteKind.APP_ROUTE,\n        page: \"/api/analyze-weather/route\",\n        pathname: \"/api/analyze-weather\",\n        filename: \"route\",\n        bundlePath: \"app/api/analyze-weather/route\"\n    },\n    resolvedPagePath: \"/app/app/api/analyze-weather/route.ts\",\n    nextConfigOutput,\n    userland: _app_app_api_analyze_weather_route_ts__WEBPACK_IMPORTED_MODULE_3__\n});\n// Pull out the exports that we need to expose from the module. This should\n// be eliminated when we've moved the other routes to the new format. These\n// are used to hook into the route.\nconst { requestAsyncStorage, staticGenerationAsyncStorage, serverHooks, headerHooks, staticGenerationBailout } = routeModule;\nconst originalPathname = \"/api/analyze-weather/route\";\nfunction patchFetch() {\n    return (0,next_dist_server_lib_patch_fetch__WEBPACK_IMPORTED_MODULE_2__.patchFetch)({\n        serverHooks,\n        staticGenerationAsyncStorage\n    });\n}\n\n\n//# sourceMappingURL=app-route.js.map//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKHJzYykvLi9ub2RlX21vZHVsZXMvbmV4dC9kaXN0L2J1aWxkL3dlYnBhY2svbG9hZGVycy9uZXh0LWFwcC1sb2FkZXIuanM/bmFtZT1hcHAlMkZhcGklMkZhbmFseXplLXdlYXRoZXIlMkZyb3V0ZSZwYWdlPSUyRmFwaSUyRmFuYWx5emUtd2VhdGhlciUyRnJvdXRlJmFwcFBhdGhzPSZwYWdlUGF0aD1wcml2YXRlLW5leHQtYXBwLWRpciUyRmFwaSUyRmFuYWx5emUtd2VhdGhlciUyRnJvdXRlLnRzJmFwcERpcj0lMkZhcHAlMkZhcHAmcGFnZUV4dGVuc2lvbnM9dHN4JnBhZ2VFeHRlbnNpb25zPXRzJnBhZ2VFeHRlbnNpb25zPWpzeCZwYWdlRXh0ZW5zaW9ucz1qcyZyb290RGlyPSUyRmFwcCZpc0Rldj10cnVlJnRzY29uZmlnUGF0aD10c2NvbmZpZy5qc29uJmJhc2VQYXRoPSZhc3NldFByZWZpeD0mbmV4dENvbmZpZ091dHB1dD0mcHJlZmVycmVkUmVnaW9uPSZtaWRkbGV3YXJlQ29uZmlnPWUzMCUzRCEiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBc0c7QUFDdkM7QUFDYztBQUNYO0FBQ2xFO0FBQ0E7QUFDQTtBQUNBLHdCQUF3QixnSEFBbUI7QUFDM0M7QUFDQSxjQUFjLHlFQUFTO0FBQ3ZCO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQSxZQUFZO0FBQ1osQ0FBQztBQUNEO0FBQ0E7QUFDQTtBQUNBLFFBQVEsdUdBQXVHO0FBQy9HO0FBQ0E7QUFDQSxXQUFXLDRFQUFXO0FBQ3RCO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDNko7O0FBRTdKIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vcGluZWxhbmRzLXdpbGRmaXJlLWFwcC8/ZDY1YSJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgeyBBcHBSb3V0ZVJvdXRlTW9kdWxlIH0gZnJvbSBcIm5leHQvZGlzdC9zZXJ2ZXIvZnV0dXJlL3JvdXRlLW1vZHVsZXMvYXBwLXJvdXRlL21vZHVsZS5jb21waWxlZFwiO1xuaW1wb3J0IHsgUm91dGVLaW5kIH0gZnJvbSBcIm5leHQvZGlzdC9zZXJ2ZXIvZnV0dXJlL3JvdXRlLWtpbmRcIjtcbmltcG9ydCB7IHBhdGNoRmV0Y2ggYXMgX3BhdGNoRmV0Y2ggfSBmcm9tIFwibmV4dC9kaXN0L3NlcnZlci9saWIvcGF0Y2gtZmV0Y2hcIjtcbmltcG9ydCAqIGFzIHVzZXJsYW5kIGZyb20gXCIvYXBwL2FwcC9hcGkvYW5hbHl6ZS13ZWF0aGVyL3JvdXRlLnRzXCI7XG4vLyBXZSBpbmplY3QgdGhlIG5leHRDb25maWdPdXRwdXQgaGVyZSBzbyB0aGF0IHdlIGNhbiB1c2UgdGhlbSBpbiB0aGUgcm91dGVcbi8vIG1vZHVsZS5cbmNvbnN0IG5leHRDb25maWdPdXRwdXQgPSBcIlwiXG5jb25zdCByb3V0ZU1vZHVsZSA9IG5ldyBBcHBSb3V0ZVJvdXRlTW9kdWxlKHtcbiAgICBkZWZpbml0aW9uOiB7XG4gICAgICAgIGtpbmQ6IFJvdXRlS2luZC5BUFBfUk9VVEUsXG4gICAgICAgIHBhZ2U6IFwiL2FwaS9hbmFseXplLXdlYXRoZXIvcm91dGVcIixcbiAgICAgICAgcGF0aG5hbWU6IFwiL2FwaS9hbmFseXplLXdlYXRoZXJcIixcbiAgICAgICAgZmlsZW5hbWU6IFwicm91dGVcIixcbiAgICAgICAgYnVuZGxlUGF0aDogXCJhcHAvYXBpL2FuYWx5emUtd2VhdGhlci9yb3V0ZVwiXG4gICAgfSxcbiAgICByZXNvbHZlZFBhZ2VQYXRoOiBcIi9hcHAvYXBwL2FwaS9hbmFseXplLXdlYXRoZXIvcm91dGUudHNcIixcbiAgICBuZXh0Q29uZmlnT3V0cHV0LFxuICAgIHVzZXJsYW5kXG59KTtcbi8vIFB1bGwgb3V0IHRoZSBleHBvcnRzIHRoYXQgd2UgbmVlZCB0byBleHBvc2UgZnJvbSB0aGUgbW9kdWxlLiBUaGlzIHNob3VsZFxuLy8gYmUgZWxpbWluYXRlZCB3aGVuIHdlJ3ZlIG1vdmVkIHRoZSBvdGhlciByb3V0ZXMgdG8gdGhlIG5ldyBmb3JtYXQuIFRoZXNlXG4vLyBhcmUgdXNlZCB0byBob29rIGludG8gdGhlIHJvdXRlLlxuY29uc3QgeyByZXF1ZXN0QXN5bmNTdG9yYWdlLCBzdGF0aWNHZW5lcmF0aW9uQXN5bmNTdG9yYWdlLCBzZXJ2ZXJIb29rcywgaGVhZGVySG9va3MsIHN0YXRpY0dlbmVyYXRpb25CYWlsb3V0IH0gPSByb3V0ZU1vZHVsZTtcbmNvbnN0IG9yaWdpbmFsUGF0aG5hbWUgPSBcIi9hcGkvYW5hbHl6ZS13ZWF0aGVyL3JvdXRlXCI7XG5mdW5jdGlvbiBwYXRjaEZldGNoKCkge1xuICAgIHJldHVybiBfcGF0Y2hGZXRjaCh7XG4gICAgICAgIHNlcnZlckhvb2tzLFxuICAgICAgICBzdGF0aWNHZW5lcmF0aW9uQXN5bmNTdG9yYWdlXG4gICAgfSk7XG59XG5leHBvcnQgeyByb3V0ZU1vZHVsZSwgcmVxdWVzdEFzeW5jU3RvcmFnZSwgc3RhdGljR2VuZXJhdGlvbkFzeW5jU3RvcmFnZSwgc2VydmVySG9va3MsIGhlYWRlckhvb2tzLCBzdGF0aWNHZW5lcmF0aW9uQmFpbG91dCwgb3JpZ2luYWxQYXRobmFtZSwgcGF0Y2hGZXRjaCwgIH07XG5cbi8vIyBzb3VyY2VNYXBwaW5nVVJMPWFwcC1yb3V0ZS5qcy5tYXAiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=\n//# sourceURL=webpack-internal:///(rsc)/./node_modules/next/dist/build/webpack/loaders/next-app-loader.js?name=app%2Fapi%2Fanalyze-weather%2Froute&page=%2Fapi%2Fanalyze-weather%2Froute&appPaths=&pagePath=private-next-app-dir%2Fapi%2Fanalyze-weather%2Froute.ts&appDir=%2Fapp%2Fapp&pageExtensions=tsx&pageExtensions=ts&pageExtensions=jsx&pageExtensions=js&rootDir=%2Fapp&isDev=true&tsconfigPath=tsconfig.json&basePath=&assetPrefix=&nextConfigOutput=&preferredRegion=&middlewareConfig=e30%3D!\n");

/***/ }),

/***/ "(rsc)/./app/api/analyze-weather/route.ts":
/*!******************************************!*\
  !*** ./app/api/analyze-weather/route.ts ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   POST: () => (/* binding */ POST)\n/* harmony export */ });\n/* harmony import */ var next_server__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! next/server */ \"(rsc)/./node_modules/next/dist/api/server.js\");\n/* harmony import */ var openai__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! openai */ \"(rsc)/./node_modules/openai/index.mjs\");\n\n\nconst openai = new openai__WEBPACK_IMPORTED_MODULE_1__[\"default\"]({\n    apiKey: process.env.OPENAI_API_KEY\n});\nasync function POST(req) {\n    try {\n        const weatherData = await req.json();\n        const response = await openai.chat.completions.create({\n            model: \"gpt-4\",\n            messages: [\n                {\n                    role: \"system\",\n                    content: `You are a wildfire risk assessment expert specializing in weather conditions.\n          Analyze weather data and provide clear, actionable insights about fire risk levels.\n          Include specific precautions based on current conditions.`\n                },\n                {\n                    role: \"user\",\n                    content: `Analyze these weather conditions for fire risk:\n          - Temperature: ${weatherData.temperature}°F\n          - Humidity: ${weatherData.humidity}%\n          - Wind Speed: ${weatherData.windSpeed} mph\n          - Wind Direction: ${weatherData.windDirection}\n          - Precipitation: ${weatherData.precipitation} inches\n          \n          Provide:\n          1. Current fire risk level\n          2. Specific concerns based on conditions\n          3. Recommended precautions\n          4. Forecast implications`\n                }\n            ],\n            max_tokens: 500\n        });\n        return next_server__WEBPACK_IMPORTED_MODULE_0__.NextResponse.json({\n            analysis: response.choices[0].message.content\n        });\n    } catch (error) {\n        console.error(\"Error:\", error);\n        return next_server__WEBPACK_IMPORTED_MODULE_0__.NextResponse.json({\n            error: \"Failed to analyze weather risk\"\n        }, {\n            status: 500\n        });\n    }\n}\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKHJzYykvLi9hcHAvYXBpL2FuYWx5emUtd2VhdGhlci9yb3V0ZS50cyIsIm1hcHBpbmdzIjoiOzs7Ozs7QUFBdUQ7QUFDNUI7QUFFM0IsTUFBTUUsU0FBUyxJQUFJRCw4Q0FBTUEsQ0FBQztJQUN4QkUsUUFBUUMsUUFBUUMsR0FBRyxDQUFDQyxjQUFBQTtBQUN0QjtBQVVPLGVBQWVDLEtBQUtDLEdBQWdCO0lBQ3pDLElBQUk7UUFDRixNQUFNQyxjQUFjLE1BQU1ELElBQUlFLElBQUk7UUFFbEMsTUFBTUMsV0FBVyxNQUFNVCxPQUFPVSxJQUFJLENBQUNDLFdBQVcsQ0FBQ0MsTUFBTSxDQUFDO1lBQ3BEQyxPQUFPO1lBQ1BDLFVBQVU7Z0JBQ1I7b0JBQ0VDLE1BQU07b0JBQ05DLFNBQVU7O21FQUVwQjtnQkFDUTtnQkFDQTtvQkFDRUQsTUFBTTtvQkFDTkMsU0FBVTt5QkFDcEIsRUFBMkJULFlBQVlVLFdBQVk7c0JBQ25ELEVBQXdCVixZQUFZVyxRQUFTO3dCQUM3QyxFQUEwQlgsWUFBWVksU0FBVTs0QkFDaEQsRUFBOEJaLFlBQVlhLGFBQWM7MkJBQ3hELEVBQTZCYixZQUFZYyxhQUFjOzs7Ozs7a0NBTXZEO2dCQUNRO2FBQ0Q7WUFDREMsWUFBWTtRQUNkO1FBRUEsT0FBT3hCLHFEQUFZQSxDQUFDVSxJQUFJLENBQUM7WUFDdkJlLFVBQVVkLFNBQVNlLE9BQU8sQ0FBQyxFQUFFLENBQUNDLE9BQU8sQ0FBQ1QsT0FBQUE7UUFDeEM7SUFDRixFQUFFLE9BQU9VLE9BQU87UUFDZEMsUUFBUUQsS0FBSyxDQUFDLFVBQVVBO1FBQ3hCLE9BQU81QixxREFBWUEsQ0FBQ1UsSUFBSSxDQUN0QjtZQUFFa0IsT0FBTztRQUFpQyxHQUMxQztZQUFFRSxRQUFRO1FBQUk7SUFFbEI7QUFDRiIsInNvdXJjZXMiOlsid2VicGFjazovL3BpbmVsYW5kcy13aWxkZmlyZS1hcHAvLi9hcHAvYXBpL2FuYWx5emUtd2VhdGhlci9yb3V0ZS50cz82ODk5Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCB7IE5leHRSZXF1ZXN0LCBOZXh0UmVzcG9uc2UgfSBmcm9tICduZXh0L3NlcnZlcic7XG5pbXBvcnQgT3BlbkFJIGZyb20gJ29wZW5haSc7XG5cbmNvbnN0IG9wZW5haSA9IG5ldyBPcGVuQUkoe1xuICBhcGlLZXk6IHByb2Nlc3MuZW52Lk9QRU5BSV9BUElfS0VZLFxufSk7XG5cbmludGVyZmFjZSBXZWF0aGVyRGF0YSB7XG4gIHRlbXBlcmF0dXJlOiBudW1iZXI7XG4gIGh1bWlkaXR5OiBudW1iZXI7XG4gIHdpbmRTcGVlZDogbnVtYmVyO1xuICB3aW5kRGlyZWN0aW9uOiBudW1iZXI7XG4gIHByZWNpcGl0YXRpb246IG51bWJlcjtcbn1cblxuZXhwb3J0IGFzeW5jIGZ1bmN0aW9uIFBPU1QocmVxOiBOZXh0UmVxdWVzdCk6IFByb21pc2U8TmV4dFJlc3BvbnNlPiB7XG4gIHRyeSB7XG4gICAgY29uc3Qgd2VhdGhlckRhdGEgPSBhd2FpdCByZXEuanNvbigpIGFzIFdlYXRoZXJEYXRhO1xuXG4gICAgY29uc3QgcmVzcG9uc2UgPSBhd2FpdCBvcGVuYWkuY2hhdC5jb21wbGV0aW9ucy5jcmVhdGUoe1xuICAgICAgbW9kZWw6IFwiZ3B0LTRcIixcbiAgICAgIG1lc3NhZ2VzOiBbXG4gICAgICAgIHtcbiAgICAgICAgICByb2xlOiBcInN5c3RlbVwiLFxuICAgICAgICAgIGNvbnRlbnQ6IGBZb3UgYXJlIGEgd2lsZGZpcmUgcmlzayBhc3Nlc3NtZW50IGV4cGVydCBzcGVjaWFsaXppbmcgaW4gd2VhdGhlciBjb25kaXRpb25zLlxuICAgICAgICAgIEFuYWx5emUgd2VhdGhlciBkYXRhIGFuZCBwcm92aWRlIGNsZWFyLCBhY3Rpb25hYmxlIGluc2lnaHRzIGFib3V0IGZpcmUgcmlzayBsZXZlbHMuXG4gICAgICAgICAgSW5jbHVkZSBzcGVjaWZpYyBwcmVjYXV0aW9ucyBiYXNlZCBvbiBjdXJyZW50IGNvbmRpdGlvbnMuYFxuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgcm9sZTogXCJ1c2VyXCIsXG4gICAgICAgICAgY29udGVudDogYEFuYWx5emUgdGhlc2Ugd2VhdGhlciBjb25kaXRpb25zIGZvciBmaXJlIHJpc2s6XG4gICAgICAgICAgLSBUZW1wZXJhdHVyZTogJHt3ZWF0aGVyRGF0YS50ZW1wZXJhdHVyZX3CsEZcbiAgICAgICAgICAtIEh1bWlkaXR5OiAke3dlYXRoZXJEYXRhLmh1bWlkaXR5fSVcbiAgICAgICAgICAtIFdpbmQgU3BlZWQ6ICR7d2VhdGhlckRhdGEud2luZFNwZWVkfSBtcGhcbiAgICAgICAgICAtIFdpbmQgRGlyZWN0aW9uOiAke3dlYXRoZXJEYXRhLndpbmREaXJlY3Rpb259XG4gICAgICAgICAgLSBQcmVjaXBpdGF0aW9uOiAke3dlYXRoZXJEYXRhLnByZWNpcGl0YXRpb259IGluY2hlc1xuICAgICAgICAgIFxuICAgICAgICAgIFByb3ZpZGU6XG4gICAgICAgICAgMS4gQ3VycmVudCBmaXJlIHJpc2sgbGV2ZWxcbiAgICAgICAgICAyLiBTcGVjaWZpYyBjb25jZXJucyBiYXNlZCBvbiBjb25kaXRpb25zXG4gICAgICAgICAgMy4gUmVjb21tZW5kZWQgcHJlY2F1dGlvbnNcbiAgICAgICAgICA0LiBGb3JlY2FzdCBpbXBsaWNhdGlvbnNgXG4gICAgICAgIH1cbiAgICAgIF0sXG4gICAgICBtYXhfdG9rZW5zOiA1MDAsXG4gICAgfSk7XG5cbiAgICByZXR1cm4gTmV4dFJlc3BvbnNlLmpzb24oeyBcbiAgICAgIGFuYWx5c2lzOiByZXNwb25zZS5jaG9pY2VzWzBdLm1lc3NhZ2UuY29udGVudCBcbiAgICB9KTtcbiAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICBjb25zb2xlLmVycm9yKCdFcnJvcjonLCBlcnJvcik7XG4gICAgcmV0dXJuIE5leHRSZXNwb25zZS5qc29uKFxuICAgICAgeyBlcnJvcjogJ0ZhaWxlZCB0byBhbmFseXplIHdlYXRoZXIgcmlzaycgfSxcbiAgICAgIHsgc3RhdHVzOiA1MDAgfVxuICAgICk7XG4gIH1cbn1cbiJdLCJuYW1lcyI6WyJOZXh0UmVzcG9uc2UiLCJPcGVuQUkiLCJvcGVuYWkiLCJhcGlLZXkiLCJwcm9jZXNzIiwiZW52IiwiT1BFTkFJX0FQSV9LRVkiLCJQT1NUIiwicmVxIiwid2VhdGhlckRhdGEiLCJqc29uIiwicmVzcG9uc2UiLCJjaGF0IiwiY29tcGxldGlvbnMiLCJjcmVhdGUiLCJtb2RlbCIsIm1lc3NhZ2VzIiwicm9sZSIsImNvbnRlbnQiLCJ0ZW1wZXJhdHVyZSIsImh1bWlkaXR5Iiwid2luZFNwZWVkIiwid2luZERpcmVjdGlvbiIsInByZWNpcGl0YXRpb24iLCJtYXhfdG9rZW5zIiwiYW5hbHlzaXMiLCJjaG9pY2VzIiwibWVzc2FnZSIsImVycm9yIiwiY29uc29sZSIsInN0YXR1cyJdLCJzb3VyY2VSb290IjoiIn0=\n//# sourceURL=webpack-internal:///(rsc)/./app/api/analyze-weather/route.ts\n");

/***/ })

};
;

// load runtime
var __webpack_require__ = require("../../../webpack-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = __webpack_require__.X(0, ["vendor-chunks/next","vendor-chunks/formdata-node","vendor-chunks/openai","vendor-chunks/form-data-encoder","vendor-chunks/whatwg-url","vendor-chunks/agentkeepalive","vendor-chunks/tr46","vendor-chunks/node-fetch","vendor-chunks/webidl-conversions","vendor-chunks/ms","vendor-chunks/humanize-ms","vendor-chunks/event-target-shim","vendor-chunks/abort-controller"], () => (__webpack_exec__("(rsc)/./node_modules/next/dist/build/webpack/loaders/next-app-loader.js?name=app%2Fapi%2Fanalyze-weather%2Froute&page=%2Fapi%2Fanalyze-weather%2Froute&appPaths=&pagePath=private-next-app-dir%2Fapi%2Fanalyze-weather%2Froute.ts&appDir=%2Fapp%2Fapp&pageExtensions=tsx&pageExtensions=ts&pageExtensions=jsx&pageExtensions=js&rootDir=%2Fapp&isDev=true&tsconfigPath=tsconfig.json&basePath=&assetPrefix=&nextConfigOutput=&preferredRegion=&middlewareConfig=e30%3D!")));
module.exports = __webpack_exports__;

})();