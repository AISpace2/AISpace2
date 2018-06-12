import * as packageJSON from "../package.json";

export * from './widget';
export const EXTENSION_SPEC_VERSION = (packageJSON as any).version;
export * from './plugin';
