import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const CentreDeCongres: React.FC = () => {
  return (
    <div id="page-centre_de_congres-0">
    <div id="imdgm" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="iy6mm" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="ipcyb" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="id7i2" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="iadn4" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centre_de_congres">{"Centre_de_congres"}</a>
          <a id="iu1mp" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/element                                                        ">{"Element"}</a>
          <a id="i7oke" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/evenement">{"Evenement"}</a>
          <a id="i4ptg" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/option">{"option"}</a>
          <a id="ivljr" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materiel">{"materiel"}</a>
          <a id="itmpk" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestation">{"prestation"}</a>
          <a id="ib9tk" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/gestionaire">{"gestionaire"}</a>
          <a id="ioa3w" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="i814l" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/indisponiblite">{"Indisponiblite"}</a>
        </div>
        <p id="ilk79" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="isj8f" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="i3oeg" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Centre_de_congres"}</h1>
        <p id="ipqr8" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage Centre_de_congres data"}</p>
        <TableBlock id="table-centre_de_congres-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Centre_de_congres List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "NomC", "column_type": "field", "field": "nomC", "type": "str", "required": true}, {"label": "Etre Reserver", "column_type": "lookup", "path": "etre_reserver", "entity": "gestionaire", "field": "liste_congres", "type": "any", "required": true}], "formColumns": [{"column_type": "field", "field": "nomC", "label": "nomC", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "etre_reserver", "field": "etre_reserver", "lookup_field": "liste_congres", "entity": "gestionaire", "type": "str", "required": true}]}} dataBinding={{"entity": "Centre_de_congres", "endpoint": "/centre_de_congres/"}} />
      </main>
    </div>    </div>
  );
};

export default CentreDeCongres;
