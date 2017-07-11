import * as widgets from "jupyter-js-widgets";
import {Graph} from "../Graph";
import SearchViewerModel from "./SearchViewerModel";

export default class SearchViewer extends widgets.DOMWidgetView {
    public model: SearchViewerModel;
    public graph: Graph;

    public render() {
        this.$el.html("<h1>hi</h1>");
    }
}
