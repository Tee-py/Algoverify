import React, { FC } from "react";
import Header from "./components/header";
import "./App.css";
import VerifyAppPage from "./components/verify";
import { Route, Routes } from "react-router-dom";
import AppList from "./components/appList";

const App: FC = () => {
  return (
    <div className="App">
      <Header></Header>
      <Routes>
        <Route path="/verify" element={<VerifyAppPage></VerifyAppPage>}></Route>
        <Route path="/" element={<AppList></AppList>}></Route>
      </Routes>
    </div>
  );
};

export default App;
