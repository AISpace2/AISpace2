declare module "*.json" {
  const value: any;
  export default value;
}

declare module "*.html" {
  const value: any;
  export default value;
}

declare module "*.vue" {
  import Vue from "vue";
  export default Vue;
}

declare module "shortid" {
  export function generate(): string;
}

interface Window {
  [key: string]: any;
}
