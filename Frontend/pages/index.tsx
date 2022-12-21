import {
  Box,
  Flex,
  Text,
  IconButton,
  Button,
  Stack,
  Collapse,
  Icon,
  Link,
  Popover,
  PopoverTrigger,
  PopoverContent,
  useColorModeValue,
  useBreakpointValue,
  useDisclosure,
  Heading,
  Divider,
  HStack,
  Wrap,
  WrapItem,
  Container,
  Input,
  LinkBox, 
  LinkOverlay, 
} from "@chakra-ui/react";
import {
  HamburgerIcon,
  CloseIcon,
  ChevronDownIcon,
  ChevronRightIcon,
} from "@chakra-ui/icons";
import { useEffect, useState } from "react";
import Router from "next/router";

const ArticleList = ({ data }: any) => {
  const [dictValue, setDictValue] = useState('');
  const [val, setVal] = useState('');
  const handleKeyDown = (e: any) => {
    if (e.key === "Enter") {
      // e.preventDefault();
      setVal(e.target.value);
    }
  };
  const handleChange = (event: any) => {
    setVal(event.target.value)
    if (event.target.value != '') {
      console.log("aaa")
      fetchData(event.target.value)
    }
  }
  const fetchData = async (query: any) => {
    console.log('fetching', `https://somas.godata.id/search?query=${query}`)
    await fetch(`https://somas.godata.id/search?query=${query.toUpperCase()}`)
    .then(res => res.json())
    .then(data => {
      console.log(data)
      setDictValue(data)
    })
  };
  
  const listItems = Object.keys(dictValue).map((key: any) => 
  <LinkBox key={key} w='100%' p='2' borderWidth='1px' rounded='md'>
    <LinkOverlay href={`?symbol=${key}`}>
      <Text>{key} {dictValue[key]}</Text>
    </LinkOverlay>
  </LinkBox>)
  return (
    <Container
      maxW={"7xl"}
      p="12"
      backgroundColor="gray.50"
      rounded={10}
      mt={5}
    >
      <Box w="100%">
        <Input
          variant="outline"
          placeholder="Search Symbol"
          _placeholder={{ textAlign: "center", color: "gray.500" }}
          onKeyDown={handleKeyDown}
          value={val}
          onChange= {handleChange}
        />
        {val != '' && dictValue != '' && 
            <>
              {listItems}
            </>}
      </Box>
      <Heading as="h2" marginTop="5" textAlign="center">
        {data.symbol}
      </Heading>
      <Divider marginTop="5" />
      <Wrap display="flex" spacing="30px" marginTop="5">
        {data.comments.map((comment: any, index: any) => {
          return (
            <WrapItem
              flex="1"
              flexBasis="100%"
              key={index}
              width={{ base: "100" }}
            >
              <Box w="100%">
                <HStack marginTop="2" spacing="2" alignItems="center">
                  <Text fontWeight="medium">{comment.date}</Text>
                </HStack>
                <Text
                  as="p"
                  fontSize="md"
                  marginTop="2"
                  backgroundColor={
                    comment["label 1"] === 1
                      ? "red.100"
                      : comment["label 1"] === 2
                      ? "green.100"
                      : ""
                  }
                  rounded={5}
                >
                  {comment.comment}
                </Text>
              </Box>
            </WrapItem>
          );
        })}
      </Wrap>
    </Container>
  );
};
export async function getServerSideProps(context: any) {
  console.log(context.query.symbol)
  const res = await fetch(
    `https://somas.godata.id/sentiment?symbol=${context.query.symbol ? context.query.symbol : "ICBP"}&start_from=0&end_at=30`
  ).then(async (response) => {
    try {
      const data = await response.json();
      return data
    } catch (error) {
      console.log("Error happened here!");
      console.error(error);
    }
  });
  const data = res;
  return { props: { data } };
}

export default ArticleList;
