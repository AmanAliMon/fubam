import Image from 'next/image';

export function Logo() {
  return (
    <Image
      src="/fubam-logo.png"
      alt="Fubam Logo"
      width={40}
      height={40}
      priority
    />
  );
}
