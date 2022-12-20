import { Box } from "@chakra-ui/react";
import { useState } from "react";

export default function Users({ initialData }: any) {
  const [data, setData] = useState(initialData);

  const fetchData = async (res: any) => {
    const req = await fetch(
      "https://randomuser.me/api/?gender=male&results=" + res
    );
    const newData = await req.json();

    return setData(newData.results);
  };

  const handleClick = (event: any) => {
    event.preventDefault();
    fetchData(2);
  };

  return (
    <Box>
      <button onClick={handleClick}>FETCH DATA</button>
      {data.map((user: any) => {
        return (
          <div>
            {user.email}
            <img src={user.picture.medium} alt="" />
          </div>
        );
      })}
    </Box>
  );
}

Users.getInitialProps = async () => {
  const req = await fetch(
    "https://randomuser.me/api/?gender=female&results=1"
  );
  const data = await req.json();
  return { initialData: data.results };
};
