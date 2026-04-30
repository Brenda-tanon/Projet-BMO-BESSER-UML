import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Materiel: React.FC = () => {
  return (
    <div id="page-materiel-4">
    <div id="ioytmf" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="iuv4ku" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="ie3u74" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="i1gnrh" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="ijyhxl" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centre_de_congres">{"Centre_de_congres"}</a>
          <a id="inbgqx" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/element                                                        ">{"Element"}</a>
          <a id="iu0fkd" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/evenement">{"Evenement"}</a>
          <a id="izj6a6" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/option">{"option"}</a>
          <a id="ir1hj7" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materiel">{"materiel"}</a>
          <a id="icqws7" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestation">{"prestation"}</a>
          <a id="i29bwh" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/gestionaire">{"gestionaire"}</a>
          <a id="iz2a2i" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="i6u80u" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/indisponiblite">{"Indisponiblite"}</a>
        </div>
        <p id="i26i7y" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="ikf9io" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="i90hw2" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"materiel"}</h1>
        <p id="ium509" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage materiel data"}</p>
        <TableBlock id="table-materiel-4" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="materiel List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Nom", "column_type": "field", "field": "nom", "type": "str", "required": true}, {"label": "Quantite", "column_type": "field", "field": "quantite", "type": "int", "required": true}, {"label": "NomO", "column_type": "field", "field": "nomO", "type": "str", "required": true}, {"label": "Peut Etre Presente", "column_type": "lookup", "path": "peut_etre_presente", "entity": "Reservation", "field": "nom", "type": "list", "required": false}], "formColumns": [{"column_type": "field", "field": "nomO", "label": "nomO", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "nom", "label": "nom", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "quantite", "label": "quantite", "type": "int", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "peut_etre_presente", "field": "peut_etre_presente", "lookup_field": "nom", "entity": "Reservation", "type": "list", "required": false}]}} dataBinding={{"entity": "materiel", "endpoint": "/materiel/"}} />
      </main>
    </div>    </div>
  );
};

export default Materiel;
