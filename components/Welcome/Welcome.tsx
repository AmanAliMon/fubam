'use client';

import { TextAnimate } from '@gfazioli/mantine-text-animate';
import { IconBrandGithub, IconExternalLink ,IconFile} from '@tabler/icons-react';
import { Anchor, Button, Center, Code, Paper, Text, Title } from '@mantine/core';
import pack from '../../package.json';
// import { ProductHunt } from '../ProductHunt/ProductHunt';
import classes from './Welcome.module.css';

export function Welcome() {
  return (
    <>
      <Center my={64}>
        {/* <ProductHunt /> */}
      </Center>
      <Title maw="90vw" mx="auto" className={classes.title} ta="center">
        <TextAnimate
          animate="in"
          by="character"
          inherit
          variant="gradient"
          component="span"
          segmentDelay={0.2}
          duration={2}
          animation="scale"
          animateProps={{
            scaleAmount: 3,
          }}
          gradient={{ from: 'blue', to: 'goldenrod' }}
        >
          Fubam
        </TextAnimate>
                Lightweight Python Template Engine

      </Title>

      <Text c="dimmed" ta="center" size="xl" maw={580} mx="auto" mt="sm">
        Fubam is a lightweight Python framework for fast and maintainable HTML generation. With a simple layout and component system, it helps developers organize pages efficiently while promoting reusability. Built-in SEO support and optional JS/CSS inlining improve performance, and minimal accessibility enhancements ensure better user experience without complexity. Fubam focuses on clarity, speed, and flexibility, making it ideal for both beginners and experienced developers who want a clean, scalable templating solution.
    </Text>

      <Center>

                <Button
          href="https://github.com/amanalimon/fubam"
          component="a"
          rightSection={<IconExternalLink />}
          leftSection={<IconBrandGithub />}
          variant="outline"
          px={32}
          radius={256}
          size="lg"
          ml="auto"
          mr="5px"
          mt="xl"
        >
          Go to Repo
        </Button>        <Button
          href="./docs"
          component="a"
          rightSection={<IconExternalLink />}
          leftSection={<IconFile />}
          variant="fill"
          px={32}
          radius={256}
          size="lg"
          mr="auto"
          ml="5px"
          mt="xl"
        >
          View Docs
        </Button>
      </Center>
{//This is temporary
}
<br /><br /><br /><br /><br />      {/*<Paper shadow="xl" p={8} mih={300} my={32} bg="dark.9" mx="auto" radius={8}>
        <TextAnimate.Typewriter
          inherit
          fz={11}
          c="green.5"
          ff="monospace"
          multiline
          delay={100}
          loop={false}
          value={[
            'Dependencies :',
            ...Object.keys(pack.dependencies).map(
              (key: string) =>
                `${key} : ${pack.dependencies[key as keyof typeof pack.dependencies].toString()}`
            ),
          ]}
        />
      </Paper>*/}
    </>
  );
}
