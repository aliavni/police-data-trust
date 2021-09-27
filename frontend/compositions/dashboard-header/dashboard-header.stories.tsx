import React from 'react'
import { ComponentStory, ComponentMeta } from '@storybook/react'
import { DashboardHeader } from '..'

export default {
  title: 'Compositions/Header',
  component: DashboardHeader
} as ComponentMeta<typeof DashboardHeader>

const Template: ComponentStory<typeof DashboardHeader> = (args) => <DashboardHeader {...args} />

export const Header = Template.bind({});
Header.args = {}
