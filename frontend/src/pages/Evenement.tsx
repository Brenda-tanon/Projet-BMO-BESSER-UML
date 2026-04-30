import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Evenement: React.FC = () => {
  return (
    <div id="page-evenement-2">
    <div id="ige4a6" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="inuq08" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="i54isb" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="isgx1k" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="i7wqj4" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centre_de_congres">{"Centre_de_congres"}</a>
          <a id="ikzpwu" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/element                                                        ">{"Element"}</a>
          <a id="ihvpkz" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/evenement">{"Evenement"}</a>
          <a id="ibzrw6" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/option">{"option"}</a>
          <a id="ipudoo" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materiel">{"materiel"}</a>
          <a id="inp6g1" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestation">{"prestation"}</a>
          <a id="iqeu26" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/gestionaire">{"gestionaire"}</a>
          <a id="iv0ygi" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="i2z3of" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/indisponiblite">{"Indisponiblite"}</a>
        </div>
        <p id="i97zq9" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="is1ywa" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="io56j3" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Evenement"}</h1>
        <p id="i9ddhq" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage Evenement data"}</p>
        <TableBlock id="table-evenement-2" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Evenement List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "NomEve", "column_type": "field", "field": "nomEve", "type": "str", "required": true}, {"label": "Description", "column_type": "field", "field": "description", "type": "str", "required": true}, {"label": "Nbpartion", "column_type": "field", "field": "nbpartion", "type": "int", "required": true}, {"label": "EmailReferent", "column_type": "field", "field": "emailReferent", "type": "str", "required": true}, {"label": "Etre Faite", "column_type": "lookup", "path": "etre_faite", "entity": "Reservation", "field": "nom", "type": "str", "required": false}], "formColumns": [{"column_type": "field", "field": "nomEve", "label": "nomEve", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "description", "label": "description", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "nbpartion", "label": "nbpartion", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "emailReferent", "label": "emailReferent", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "etre_faite", "field": "etre_faite", "lookup_field": "nom", "entity": "Reservation", "type": "str", "required": false}]}} dataBinding={{"entity": "Evenement", "endpoint": "/evenement/"}} />
      </main>
    </div>    </div>
  );
};

export default Evenement;
