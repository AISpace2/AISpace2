/**
 * List all commonly used but rarely changing dependencies here.
 * 
 * By running `npm run build:dev-dll`, it will generate a DLL used for development
 * that improves build times by not re-building and re-bundling these libraries
 * into the main chunk. Any imported library not listed here
 * will be bundled as normal - you do not *have* to list libraries here.
 * 
 * It is currently automatically run for you if you run `npm run dev` or `npm run build:dev`.
 * 
 * This file is NOT used for production.
 */

require("vue");
require("d3");
require("shortid");
require("core-js");
