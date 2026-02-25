'use client';

import { Navbar } from 'nextra-theme-docs';
import { Group, Text } from '@mantine/core';
import { ColorSchemeControl } from '../ColorSchemeControl/ColorSchemeControl';
import { Logo } from '../Logo/Logo';
import { MantineNextraThemeObserver } from '../MantineNextraThemeObserver/MantineNextraThemeObserver';

/**
 * You can customize the Nextra NavBar component.
 * Don't forget to use the MantineProvider and MantineNextraThemeObserver components.
 *
 * @since 1.0.0
 *
 */
export const MantineNavBar = () => {
  return (
    <>
      <MantineNextraThemeObserver />
      <Navbar
        logo={
          <Group align="center" gap={4}>
            <Logo />
            <Text size="lg" fw={800} c="blue" visibleFrom="xl">
Fubam            </Text>
          </Group>
        }
        // Mantine discord server
        // chatLink="https://discord.com/invite/wbH82zuWMN"
         projectLink="https://github.com/amanalimon/fubam"
      >
        <>
          <ColorSchemeControl />
          {/* <iframe
            src="https://github.com/sponsors/gfazioli/button"
            title="Donate to fubam"
            height="32"
            width="114"
            style={{ border: 0, borderRadius: '6px' }}
          /> */}
        </>
      </Navbar>
    </>
  );
};
