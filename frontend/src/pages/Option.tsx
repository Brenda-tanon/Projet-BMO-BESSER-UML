import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Option: React.FC = () => {
  return (
    <div id="page-option-3">
    <div id="i7rtw1" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="i6wyqe" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="ibpi1d" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="iit396" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="ihmtaj" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centre_de_congres">{"Centre_de_congres"}</a>
          <a id="ida315" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/element                                                        ">{"Element"}</a>
          <a id="iwzzm2" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/evenement">{"Evenement"}</a>
          <a id="i1w85b" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/option">{"option"}</a>
          <a id="i65ztl" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materiel">{"materiel"}</a>
          <a id="imltfr" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestation">{"prestation"}</a>
          <a id="ip5m2v" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/gestionaire">{"gestionaire"}</a>
          <a id="if5aag" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="i7svmk" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/indisponiblite">{"Indisponiblite"}</a>
        </div>
        <p id="icq1j7" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="iw4pyq" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="iihh5v" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"option"}</h1>
        <p id="icrrph" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage option data"}</p>
        <TableBlock id="table-option-3" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="option List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "NomO", "column_type": "field", "field": "nomO", "type": "str", "required": true}, {"label": "Peut Etre Presente", "column_type": "lookup", "path": "peut_etre_presente", "entity": "Reservation", "field": "nom", "type": "list", "required": false}], "formColumns": [{"column_type": "field", "field": "nomO", "label": "nomO", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "peut_etre_presente", "field": "peut_etre_presente", "lookup_field": "nom", "entity": "Reservation", "type": "list", "required": false}]}} dataBinding={{"entity": "option", "endpoint": "/option/"}} />
      </main>
    </div>    </div>
  );
};

export default Option;
