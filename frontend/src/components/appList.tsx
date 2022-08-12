import React, { useEffect, useState } from "react";
import { Table } from "antd";
import "antd/dist/antd.css";
import { getVerifiedApps } from "../network";
import { AppType } from "../types";

const tableColumns = [
  {
    title: "Name",
    dataIndex: "name",
    key: "name",
  },
  {
    title: "Description",
    dataIndex: "description",
    key: "description",
  },
  {
    title: "Application Type",
    dataIndex: "appType",
    key: "app-type",
  },
  {
    title: "Application ID",
    dataIndex: "appId",
    key: "app-id",
  },
  {
    title: "Github url",
    dataIndex: "githubUrl",
    key: "gh",
    render: (text: string[]) =>
      text.map((ele, key) => (
        <div key={key}>
          <a href={ele} key={key + 1} target="_blank" rel="noopener noreferrer">
            {ele}
          </a>
          <br></br>
        </div>
      )),
  },
];

const AppList = () => {
  const defaultState: AppType[] = [];
  const [tableData, setTableData] = useState(defaultState);
  useEffect(() => {
    async function fetchApps() {
      const response = await getVerifiedApps();
      let apps: AppType[] = [];
      response.map((app, key: number) =>
        apps.push({
          key: key,
          name: app.name,
          description: app.description,
          appType: app.type,
          appId: app.app_id,
          githubUrl: [app.approval_github_url, app.clear_state_github_url, app.github_url],
        })
      );
      setTableData(apps);
    }
    fetchApps();
  }, []);
  return (
    <div style={{ padding: "1rem" }}>
      <h1 style={{ margin: "1rem" }}>Verified Apps</h1>
      <Table columns={tableColumns} dataSource={tableData} />
    </div>
  );
};

export default AppList;
